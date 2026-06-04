#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "FAIL: virtual environment python not found at $PYTHON_BIN"
  exit 1
fi

cd "$ROOT_DIR"
"$PYTHON_BIN" -m unittest security.test_f2_t02_security_response

echo "PASS: F2-T02 acceptance test passed"
