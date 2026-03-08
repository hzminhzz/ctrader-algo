#!/usr/bin/env bash
set -euo pipefail

python -m pytest tests/contract -v
python -m pytest tests/integration -v
python -m pytest tests/e2e -v
python -m pytest tests/fixtures -v
