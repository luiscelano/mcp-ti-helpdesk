#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "FAIL: virtual environment python not found at $PYTHON_BIN"
  exit 1
fi

cd "$ROOT_DIR"
"$PYTHON_BIN" -m unittest tests.INGEST.test_f1_t05_ingest_e2e

echo "PASS: F1-T05 acceptance test passed"
