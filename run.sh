#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT/backend"
FRONTEND_DIR="$ROOT/frontend"
VENV_DIR="$BACKEND_DIR/.venv"
PID_DIR="$ROOT/.run"
BACKEND_PID_FILE="$PID_DIR/backend.pid"
FRONTEND_PID_FILE="$PID_DIR/frontend.pid"
BACKEND_LOG="$PID_DIR/backend.log"
FRONTEND_LOG="$PID_DIR/frontend.log"

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-3000}"

# Local SQLite by default; set USE_POSTGRES=1 to use Postgres from .env
USE_POSTGRES="${USE_POSTGRES:-0}"

mkdir -p "$PID_DIR"

info()  { printf '\033[1;34m→\033[0m %s\n' "$*"; }
ok()    { printf '\033[1;32m✓\033[0m %s\n' "$*"; }
warn()  { printf '\033[1;33m!\033[0m %s\n' "$*"; }
err()   { printf '\033[1;31m✗\033[0m %s\n' "$*" >&2; }

cleanup() {
  local code=$?
  trap - EXIT INT TERM
  info "Stopping services..."
  stop_pid_file "$FRONTEND_PID_FILE" "frontend"
  stop_pid_file "$BACKEND_PID_FILE" "backend"
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

free_port() {
  local port="$1"
  local pids
  local i

  pids="$(pids_on_port "$port")"
  if [[ -z "${pids// /}" ]]; then
    return 0
  fi

  warn "Port $port is busy — stopping process(es): $pids"
  # shellcheck disable=SC2086
  kill $pids 2>/dev/null || true

  for i in $(seq 1 20); do
    pids="$(pids_on_port "$port")"
    if [[ -z "${pids// /}" ]]; then
      return 0
    fi
    # Escalate if still holding the port.
    if [[ "$i" -eq 8 ]]; then
      # shellcheck disable=SC2086
      kill -9 $pids 2>/dev/null || true
    fi
    sleep 0.25
  done

  pids="$(pids_on_port "$port")"
  if [[ -n "${pids// /}" ]]; then
    err "Could not free port $port (still held by: $pids)"
    return 1
  fi
}

django_env() {
  # Prefer local SQLite unless Postgres is explicitly requested.
  if [[ "$USE_POSTGRES" != "1" ]]; then
    env -u POSTGRES_DB -u POSTGRES_USER -u POSTGRES_PASSWORD \
        -u POSTGRES_HOST -u POSTGRES_PORT -u DATABASE_URL \
        "$@"
  else
    set -a
    # shellcheck disable=SC1091
    [[ -f "$ROOT/.env" ]] && source "$ROOT/.env"
    set +a
    "$@"
  fi
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
NEXT_PUBLIC_API_URL=http://localhost:${BACKEND_PORT}/api
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
  npm run dev -- -p "$FRONTEND_PORT" --hostname 127.0.0.1 >"$FRONTEND_LOG" 2>&1 &
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
    if grep -qE 'Ready in|Local:' "$FRONTEND_LOG" 2>/dev/null \
      && curl -sf "http://127.0.0.1:${FRONTEND_PORT}/" >/dev/null 2>&1; then
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
}

usage() {
  cat <<EOF
Usage: ./run.sh [options]

Starts Forma Studio locally:
  1) checks for new Django migrations (makemigrations)
  2) applies pending migrations (migrate)
  3) starts backend + frontend

Options:
  --postgres     Use Postgres from .env (default: SQLite)
  --seed         Run seed_data after migrate
  --backend-only Start only Django
  --frontend-only Start only Next.js
  -h, --help     Show this help

Env:
  BACKEND_PORT=8000 FRONTEND_PORT=3000 USE_POSTGRES=0
EOF
}

SEED=0
BACKEND_ONLY=0
FRONTEND_ONLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --postgres) USE_POSTGRES=1; shift ;;
    --seed) SEED=1; shift ;;
    --backend-only) BACKEND_ONLY=1; shift ;;
    --frontend-only) FRONTEND_ONLY=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) err "Unknown option: $1"; usage; exit 1 ;;
  esac
done

trap cleanup EXIT INT TERM

info "Forma Studio — local run"
echo "  root: $ROOT"

if [[ "$FRONTEND_ONLY" -eq 0 ]]; then
  ensure_backend
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
fi

echo
ok "Project is running"
echo "  Site:   http://127.0.0.1:${FRONTEND_PORT}"
echo "  API:    http://127.0.0.1:${BACKEND_PORT}/api/home/"
echo "  Admin:  http://127.0.0.1:${BACKEND_PORT}/admin/"
echo "  Logs:   $PID_DIR/*.log"
echo
info "Press Ctrl+C to stop"

# Keep script attached while children live
while true; do
  if [[ "$FRONTEND_ONLY" -eq 0 ]] && [[ -f "$BACKEND_PID_FILE" ]] && ! kill -0 "$(cat "$BACKEND_PID_FILE")" 2>/dev/null; then
    err "Backend process exited unexpectedly. See $BACKEND_LOG"
    exit 1
  fi
  if [[ "$BACKEND_ONLY" -eq 0 ]] && [[ -f "$FRONTEND_PID_FILE" ]] && ! kill -0 "$(cat "$FRONTEND_PID_FILE")" 2>/dev/null; then
    err "Frontend process exited unexpectedly. See $FRONTEND_LOG"
    exit 1
  fi
  sleep 2
done
