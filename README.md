# cTrader Algo Pipeline

This repository is a cTrader-centered research and backtesting pipeline inspired by ZenomTrader-style workflows. It includes:

- cBot source and `.algo` build path
- Docker-based `ctrader-console` backtesting
- backtest report ingestion into ledger events
- portfolio analytics, journal projection, and prop-firm rule evaluation
- approval-gated orchestration plus Discord/tweet downstream helpers

## Non-technical customer flow

If you are not a developer, use the operator app instead of working directly with Python files, manifests, or Docker commands.

### What you do as a customer

1. open the operator app
2. describe your strategy in plain English
3. fill in the safe settings such as symbol, timeframe, and risk
4. review the generated draft and complete the checklist
5. prepare the backtest request
6. read the evaluation summary
7. check whether the strategy is ready for approval

### Start the operator app

From the repo root:

```bash
pip install "streamlit>=1.42,<2"
streamlit run apps/operator_ui/streamlit_app.py
```

### What each stage means

- **Create** — describe the strategy idea and fill in the safe config form
- **Review** — confirm the generated summary, risk, and checklist items
- **Backtest** — prepare the manifest-backed backtest command without editing files manually
- **Evaluate** — read the run summary, journal summary, metrics, and prop-style checks
- **Promote** — see whether the strategy is blocked, awaiting approval, or ready for the next approval step

### What you do not need to do

You do **not** need to:

- edit code files in `apps/` or `libs/`
- hand-write backtest manifests
- inspect raw report JSON unless you want to
- understand the repo architecture before using the workflow

### Current limit

This operator flow is a guided layer on top of the repo. It helps you create, review, and prepare strategies safely, but live promotion is still approval-gated and not fully automated.

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
