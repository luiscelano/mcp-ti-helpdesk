#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "FAIL: virtual environment python not found at $PYTHON_BIN"
  exit 1
fi

cd "$ROOT_DIR"
"$PYTHON_BIN" -m unittest \
  tests.SEC.test_sec_baseline \
  tests.CLS.test_cls_baseline \
  tests.RAG.test_rag_baseline \
  tests.GRAPH.test_graph_baseline \
  tests.PLAN.test_plan_baseline \
  tests.MCP.test_mcp_baseline \
  tests.INGEST.test_ingest_baseline \
  tests.INT.test_int_baseline

echo "PASS: F6-T01 acceptance test passed"
