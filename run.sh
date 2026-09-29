#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT/backend"
FRONTEND_DIR="$ROOT/frontend"
VENV_DIR="$BACKEND_DIR/.venv"
PID_DIR="$ROOT/.run"
BACKEND_PID_FILE="$PID_DIR/backend.pid"
FRONTEND_PID_FILE="$PID_DIR/frontend.pid"
NGROK_PID_FILE="$PID_DIR/ngrok.pid"
BACKEND_LOG="$PID_DIR/backend.log"
FRONTEND_LOG="$PID_DIR/frontend.log"
NGROK_LOG="$PID_DIR/ngrok.log"
NGROK_URL_FILE="$PID_DIR/ngrok.url"

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-3000}"
NGROK_API="${NGROK_API:-http://127.0.0.1:4040}"

# Local and Docker both use Postgres from .env (host port POSTGRES_PORT).

mkdir -p "$PID_DIR"

info()  { printf '\033[1;34m→\033[0m %s\n' "$*"; }
ok()    { printf '\033[1;32m✓\033[0m %s\n' "$*"; }
warn()  { printf '\033[1;33m!\033[0m %s\n' "$*"; }
err()   { printf '\033[1;31m✗\033[0m %s\n' "$*" >&2; }

lan_ipv4() {
  hostname -I 2>/dev/null \
    | tr ' ' '\n' \
    | grep -E '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' \
    | grep -vE '^127\.' \
    || true
}

cleanup() {
  local code=$?
  trap - EXIT INT TERM
  info "Stopping services..."
  stop_pid_file "$NGROK_PID_FILE" "ngrok"
  stop_pid_file "$FRONTEND_PID_FILE" "frontend"
  stop_pid_file "$BACKEND_PID_FILE" "backend"
  rm -f "$NGROK_URL_FILE"
  exit "$code"
}

stop_pid_file() {
  local file="$1"
  local name="$2"
  if [[ -f "$file" ]]; then
    local pid
    pid="$(cat "$file" 2>/dev/null || true)"
    if [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      wait "$pid" 2>/dev/null || true
      ok "Stopped $name (pid $pid)"
    fi
    rm -f "$file"
  fi
}

port_in_use() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -ltn 2>/dev/null | grep -qE ":${port}([[:space:]]|$)" && return 0
    return 1
  fi
  if command -v lsof >/dev/null 2>&1; then
    lsof -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1
    return $?
  fi
  return 1
}

pids_on_port() {
  local port="$1"
  local pids=""

  if command -v lsof >/dev/null 2>&1; then
    pids="$(lsof -t -iTCP:"$port" -sTCP:LISTEN 2>/dev/null | tr '\n' ' ' || true)"
  fi

  # Fallback: parse ss (works when lsof misses node/next listeners).
  if [[ -z "${pids// /}" ]] && command -v ss >/dev/null 2>&1; then
    pids="$(
      ss -ltnp 2>/dev/null \
        | grep -E ":${port}([[:space:]]|$)" \
        | grep -oE 'pid=[0-9]+' \
        | cut -d= -f2 \
        | sort -u \
        | tr '\n' ' ' || true
    )"
  fi

  # shellcheck disable=SC2086
  echo $pids
}

# Docker publishes ports via a root-owned proxy. ss/lsof then show no pid,
# so a plain "no process" check looks like the port is free.
docker_on_port() {
  local port="$1"
  command -v docker >/dev/null 2>&1 || return 0
  docker ps --format '{{.Names}} {{.Ports}}' 2>/dev/null \
    | grep -E "(0\.0\.0\.0|\[::\]|:::):${port}->" \
    | awk '{print $1}' \
    || true
}

free_port() {
  local port="$1"
  local pids
  local holders
  local i

  if ! port_in_use "$port"; then
    return 0
  fi

  holders="$(docker_on_port "$port" | tr '\n' ' ')"
  if [[ -n "${holders// /}" ]]; then
    err "Port $port is published by Docker: ${holders}"
    err "Stop it: docker stop ${holders}"
    err "Or pick another port, for example: FRONTEND_PORT=3010 ./run.sh"
    return 1
  fi

  pids="$(pids_on_port "$port")"
  if [[ -z "${pids// /}" ]]; then
    err "Port $port is in use, but this user cannot see the process (often root)."
    err "Or pick another port, for example: FRONTEND_PORT=3010 ./run.sh"
    return 1
  fi

  warn "Port $port is busy — stopping process(es): $pids"
  # shellcheck disable=SC2086
  kill $pids 2>/dev/null || true

  for i in $(seq 1 20); do
    if ! port_in_use "$port"; then
      return 0
    fi
    pids="$(pids_on_port "$port")"
    # Escalate if still holding the port.
    if [[ "$i" -eq 8 && -n "${pids// /}" ]]; then
      # shellcheck disable=SC2086
      kill -9 $pids 2>/dev/null || true
    fi
    sleep 0.25
  done

  if port_in_use "$port"; then
    pids="$(pids_on_port "$port")"
    err "Could not free port $port (still held by: ${pids:-unknown})"
    return 1
  fi
}

django_env() {
  set -a
  # shellcheck disable=SC1091
  [[ -f "$ROOT/.env" ]] && source "$ROOT/.env"
  set +a
  "$@"
}

ensure_postgres() {
  set -a
  # shellcheck disable=SC1091
  [[ -f "$ROOT/.env" ]] && source "$ROOT/.env"
  set +a
  local host="${POSTGRES_HOST:-127.0.0.1}"
  local port="${POSTGRES_PORT:-5434}"
  info "Checking Postgres on ${host}:${port}..."
  if command -v pg_isready >/dev/null 2>&1 && pg_isready -h "$host" -p "$port" >/dev/null 2>&1; then
    ok "Postgres is up"
    return 0
  fi
  if ! command -v docker >/dev/null 2>&1; then
    err "Postgres is not running on ${host}:${port} and docker is not available."
    exit 1
  fi
  info "Starting Postgres (docker compose db)..."
  docker compose -f "$ROOT/docker-compose.yml" up -d db
  local i
  for i in $(seq 1 40); do
    if command -v pg_isready >/dev/null 2>&1; then
      pg_isready -h "$host" -p "$port" >/dev/null 2>&1 && break
    else
      (echo >/dev/tcp/"$host"/"$port") >/dev/null 2>&1 && break
    fi
    sleep 0.5
  done
  if command -v pg_isready >/dev/null 2>&1 && ! pg_isready -h "$host" -p "$port" >/dev/null 2>&1; then
    err "Postgres did not become ready on ${host}:${port}"
    exit 1
  fi
  ok "Postgres → ${host}:${port}"
}

ensure_backend() {
  info "Preparing backend..."
  if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    info "Creating Python venv..."
    python3 -m venv "$VENV_DIR"
  fi
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
  pip install -q -r "$BACKEND_DIR/requirements.txt"
}

run_migrations() {
  info "Checking Django migrations..."
  cd "$BACKEND_DIR"
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"

  local pending_models=0
  if ! django_env python manage.py makemigrations --check --dry-run >/dev/null 2>&1; then
    pending_models=1
  fi

  if [[ "$pending_models" -eq 1 ]]; then
    warn "Model changes detected — creating migrations..."
    django_env python manage.py makemigrations --noinput
    ok "Migrations created"
  else
    ok "No new model changes"
  fi

  local plan
  plan="$(django_env python manage.py showmigrations --plan 2>/dev/null | grep -E '^\s*\[ \]' || true)"
  if [[ -n "$plan" ]]; then
    warn "Unapplied migrations found — applying..."
    printf '%s\n' "$plan"
    django_env python manage.py migrate --noinput
    ok "Migrations applied"
  else
    ok "Database is up to date"
  fi
}

ensure_frontend() {
  info "Preparing frontend..."
  cd "$FRONTEND_DIR"
  if [[ ! -d node_modules ]] || [[ ! -x node_modules/.bin/next ]]; then
    npm install
  fi
  if [[ ! -f .env.local ]]; then
    cat > .env.local <<EOF
NEXT_PUBLIC_API_URL=/api
INTERNAL_API_URL=http://127.0.0.1:${BACKEND_PORT}/api
NEXT_PUBLIC_SITE_URL=http://localhost:${FRONTEND_PORT}
EOF
    ok "Created frontend/.env.local"
  fi
}

start_backend() {
  info "Starting Django on :$BACKEND_PORT..."
  free_port "$BACKEND_PORT" || exit 1
  cd "$BACKEND_DIR"
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
  django_env python manage.py runserver "0.0.0.0:${BACKEND_PORT}" >"$BACKEND_LOG" 2>&1 &
  echo $! >"$BACKEND_PID_FILE"
  sleep 1
  if kill -0 "$(cat "$BACKEND_PID_FILE")" 2>/dev/null; then
    ok "Backend → http://127.0.0.1:${BACKEND_PORT}  (admin: /admin/)"
  else
    err "Backend failed to start. See $BACKEND_LOG"
    tail -n 40 "$BACKEND_LOG" || true
    exit 1
  fi
}

start_frontend() {
  info "Starting Next.js on :$FRONTEND_PORT..."
  free_port "$FRONTEND_PORT" || exit 1
  : >"$FRONTEND_LOG"
  cd "$FRONTEND_DIR"
  local extra_origins="" ip
  for ip in $(lan_ipv4); do
    extra_origins="${extra_origins:+$extra_origins,}${ip}"
  done
  ALLOWED_DEV_ORIGINS="${ALLOWED_DEV_ORIGINS:+$ALLOWED_DEV_ORIGINS,}${extra_origins}" \
    npm run dev -- -p "$FRONTEND_PORT" --hostname 0.0.0.0 >"$FRONTEND_LOG" 2>&1 &
  echo $! >"$FRONTEND_PID_FILE"

  # Wait until our process is alive AND Next reports Ready (not a leftover server).
  local i
  local ready=0
  for i in $(seq 1 60); do
    if ! kill -0 "$(cat "$FRONTEND_PID_FILE")" 2>/dev/null; then
      err "Frontend failed to start. See $FRONTEND_LOG"
      tail -n 40 "$FRONTEND_LOG" || true
      exit 1
    fi
    local http_code=""
    if grep -qE 'Ready in|Local:' "$FRONTEND_LOG" 2>/dev/null; then
      http_code="$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:${FRONTEND_PORT}/" || true)"
    fi
    # 401 is the site gate (basic auth), not a failed server.
    if [[ "$http_code" =~ ^[2345] ]]; then
      ready=1
      break
    fi
    if grep -qE 'EADDRINUSE|Failed to start server' "$FRONTEND_LOG" 2>/dev/null; then
      err "Frontend failed to bind :$FRONTEND_PORT. See $FRONTEND_LOG"
      tail -n 40 "$FRONTEND_LOG" || true
      exit 1
    fi
    sleep 0.5
  done

  if [[ "$ready" -ne 1 ]]; then
    err "Frontend did not become ready in time. See $FRONTEND_LOG"
    tail -n 40 "$FRONTEND_LOG" || true
    exit 1
  fi

  ok "Frontend → http://127.0.0.1:${FRONTEND_PORT}"

  # Next.js may replace the npm wrapper with a child that keeps :3000.
  local listen_pid
  listen_pid="$(pids_on_port "$FRONTEND_PORT" | awk '{print $1}')"
  if [[ -n "${listen_pid:-}" ]]; then
    echo "$listen_pid" >"$FRONTEND_PID_FILE"
  fi
}

ngrok_public_url() {
  curl -sf "${NGROK_API}/api/tunnels" 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    raise SystemExit(0)
tunnels = data.get('tunnels') or []
https = next((t.get('public_url') or '' for t in tunnels if str(t.get('public_url','')).startswith('https')), '')
print(https or next((t.get('public_url') or '' for t in tunnels if t.get('public_url')), ''))
" 2>/dev/null || true
}

start_ngrok() {
  if [[ "$SKIP_NGROK" -eq 1 ]]; then
    return 0
  fi
  if ! command -v ngrok >/dev/null 2>&1; then
    warn "ngrok not found in PATH — skip public URL"
    return 0
  fi

  info "Starting ngrok tunnel → :$FRONTEND_PORT..."
  pkill -f "ngrok http" >/dev/null 2>&1 || true
  sleep 0.4
  free_port 4040 || true
  : >"$NGROK_LOG"
  rm -f "$NGROK_URL_FILE"

  # ngrok 3.x: flags like --host-header were removed; keep the command compatible.
  # Optional reserved domain: NGROK_URL=https://your-name.ngrok-free.dev
  local ngrok_args=(http "http://127.0.0.1:${FRONTEND_PORT}" --log=stdout)
  if [[ -n "${NGROK_URL:-}" ]]; then
    ngrok_args+=(--url "$NGROK_URL")
  fi
  ngrok "${ngrok_args[@]}" >"$NGROK_LOG" 2>&1 &
  echo $! >"$NGROK_PID_FILE"

  local i url=""
  for i in $(seq 1 40); do
    if ! kill -0 "$(cat "$NGROK_PID_FILE")" 2>/dev/null; then
      err "ngrok failed to start. See $NGROK_LOG"
      tail -n 40 "$NGROK_LOG" || true
      return 1
    fi
    url="$(ngrok_public_url)"
    if [[ -n "${url:-}" ]]; then
      printf '%s\n' "$url" >"$NGROK_URL_FILE"
      ok "Public → $url"
      echo "  Phone: open this URL, then tap Visit Site once (free ngrok warning)."
      return 0
    fi
    sleep 0.25
  done

  warn "ngrok is running, but public URL is not ready yet. See $NGROK_LOG"
}

usage() {
  cat <<EOF
Usage: ./run.sh [options]

Starts Forma Studio locally:
  1) checks for new Django migrations (makemigrations)
  2) applies pending migrations (migrate)
  3) starts backend + frontend
  4) starts ngrok public URL (unless --no-ngrok)

Options:
  --seed          Run seed_data after migrate
  --backend-only  Start only Django
  --frontend-only Start only Next.js
  --no-ngrok      Do not start the public ngrok tunnel
  -h, --help      Show this help

Env:
  BACKEND_PORT=8000 FRONTEND_PORT=3000
  NGROK_URL=https://your-name.ngrok-free.dev   # pin reserved domain (optional)
EOF
}

SEED=0
BACKEND_ONLY=0
FRONTEND_ONLY=0
SKIP_NGROK=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --seed) SEED=1; shift ;;
    --backend-only) BACKEND_ONLY=1; shift ;;
    --frontend-only) FRONTEND_ONLY=1; shift ;;
    --no-ngrok) SKIP_NGROK=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) err "Unknown option: $1"; usage; exit 1 ;;
  esac
done

trap cleanup EXIT INT TERM

info "Forma Studio — local run"
echo "  root: $ROOT"

if [[ "$FRONTEND_ONLY" -eq 0 ]]; then
  ensure_backend
  ensure_postgres
  run_migrations
  if [[ "$SEED" -eq 1 ]]; then
    info "Seeding demo data..."
    cd "$BACKEND_DIR"
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    django_env python manage.py seed_data
    ok "Seed complete"
  fi
  start_backend
fi

if [[ "$BACKEND_ONLY" -eq 0 ]]; then
  ensure_frontend
  start_frontend
  start_ngrok || true
fi

echo
ok "Project is running"
echo "  Site:   http://127.0.0.1:${FRONTEND_PORT}"
for lan in $(lan_ipv4); do
  echo "  LAN:    http://${lan}:${FRONTEND_PORT}  (same Wi-Fi as this PC)"
done
echo "  API:    http://127.0.0.1:${BACKEND_PORT}/api/home/"
echo "  Admin:  http://127.0.0.1:${BACKEND_PORT}/admin/"
if [[ -f "$NGROK_URL_FILE" ]]; then
  echo "  Mobile (ngrok): $(cat "$NGROK_URL_FILE")"
  echo "    Free ngrok shows a warning — tap Visit Site once, then reload."
fi
echo "  Logs:   $PID_DIR/*.log"
echo
info "Press Ctrl+C to stop"

# Keep script attached while children live
frontend_misses=0
while true; do
  if [[ "$FRONTEND_ONLY" -eq 0 ]] && [[ -f "$BACKEND_PID_FILE" ]] && ! kill -0 "$(cat "$BACKEND_PID_FILE")" 2>/dev/null; then
    err "Backend process exited unexpectedly. See $BACKEND_LOG"
    exit 1
  fi
  if [[ "$BACKEND_ONLY" -eq 0 ]]; then
    if [[ -f "$FRONTEND_PID_FILE" ]] && kill -0 "$(cat "$FRONTEND_PID_FILE")" 2>/dev/null; then
      frontend_misses=0
    elif port_in_use "$FRONTEND_PORT"; then
      pids_on_port "$FRONTEND_PORT" | awk '{print $1}' >"$FRONTEND_PID_FILE"
      frontend_misses=0
    else
      frontend_misses=$((frontend_misses + 1))
      if [[ "$frontend_misses" -ge 4 ]]; then
        err "Frontend process exited unexpectedly. See $FRONTEND_LOG"
        exit 1
      fi
    fi
  fi
  if [[ "$SKIP_NGROK" -eq 0 ]] && [[ -f "$NGROK_PID_FILE" ]] && ! kill -0 "$(cat "$NGROK_PID_FILE")" 2>/dev/null; then
    warn "ngrok exited. See $NGROK_LOG"
    rm -f "$NGROK_PID_FILE" "$NGROK_URL_FILE"
  fi
  sleep 2
done
