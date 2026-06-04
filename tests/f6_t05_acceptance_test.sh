#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "FAIL: virtual environment python not found at $PYTHON_BIN"
  exit 1
fi

cd "$ROOT_DIR"

./tests/f6_t01_acceptance_test.sh
./tests/f6_t02_acceptance_test.sh
./tests/f6_t03_acceptance_test.sh
./tests/f6_t04_acceptance_test.sh
"$PYTHON_BIN" -m unittest tests.DELIVERY.test_f6_t05_delivery_candidate

echo "PASS: F6-T05 acceptance test passed"
