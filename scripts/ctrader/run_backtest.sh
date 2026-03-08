#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: run_backtest.sh <manifest-path>"
  exit 1
fi

python -c "from apps.orchestrator.ctrader_cli import build_backtest_command; print(' '.join(build_backtest_command('$1')))"
