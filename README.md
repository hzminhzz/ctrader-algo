# cTrader Algo Pipeline

This repository is a cTrader-centered research and backtesting pipeline inspired by ZenomTrader-style workflows. It includes:

- cBot source and `.algo` build path
- Docker-based `ctrader-console` backtesting
- backtest report ingestion into ledger events
- portfolio analytics, journal projection, and prop-firm rule evaluation
- approval-gated orchestration plus Discord/tweet downstream helpers

## Quick start

Read these in order:

1. `docs/guides/vps-download-and-run.md`
2. `docs/runbooks/ctrader-cli-environment.md`
3. `docs/runbooks/ctrader-backtest-smoke.md`
4. `docs/runbooks/promotion-gates.md`

## What is already verified

- `.algo` packaging works from `ctrader/bots/BreakoutBot/`
- Docker `ghcr.io/spotware/ctrader-console:latest` works for metadata and backtest runs
- runtime reports can be captured as HTML/JSON
- ingestion, analytics, journal, prop rules, workflow gates, Discord filtering, tweet drafts, and CI smoke checks are implemented and tested

## Main directories

- `ctrader/bots/BreakoutBot/` — cBot source and parameters
- `ctrader/cli/` — runtime and backtest manifest area
- `apps/` — orchestrator, ledger, analytics, journal, prop simulator, Discord, content pipeline
- `libs/` — shared contracts, report parsing, LLM validation
- `docs/` — architecture, runbooks, VPS/setup guides
- `tests/` — contract, integration, fixture, and e2e tests

## Local verification

```bash
python -m pytest tests/contract -v
python -m pytest tests/integration -v
python -m pytest tests/e2e -v
python -m pytest tests/fixtures -v
bash scripts/ci/smoke.sh
```
