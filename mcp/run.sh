#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$DIR/.venv/bin/python"

if [[ ! -x "$PY" ]]; then
  echo "Не знайдено $PY" >&2
  echo "Один раз встановіть залежності:" >&2
  echo "  python3 -m venv mcp/.venv && mcp/.venv/bin/pip install -r mcp/requirements.txt" >&2
  exit 1
fi

exec "$PY" "$DIR/server.py"
