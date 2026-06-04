#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "FAIL: virtual environment python not found at $PYTHON_BIN"
  exit 1
fi

cd "$ROOT_DIR"
"$PYTHON_BIN" -m unittest graph_rag.test_f3_t03_search_graph

echo "PASS: F3-T03 acceptance test passed"
