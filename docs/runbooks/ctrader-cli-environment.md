# cTrader CLI Environment Contract

## Supported cTrader version

- Supported cTrader CLI version: target the installed CLI version that matches the local desktop or VPS cTrader environment used for smoke runs.

## Runner OS

- Runner OS: Linux or macOS shell environment for orchestration.
- Shell: POSIX-compatible shell.

## Required installed components

- cTrader CLI installed and available on `PATH`.
- .NET SDK installed for local cBot build verification.
- Python environment for orchestration utilities and tests.

## Artifact directories

- Backtest manifests: `ctrader/cli/backtest-manifests/`
- Backtest report fixtures: `tests/fixtures/reports/`
- cBot parameter files: `ctrader/bots/BreakoutBot/Parameters/`

## Parameter file locations

- Smoke parameter set: `ctrader/bots/BreakoutBot/Parameters/smoke.cbotset`

## JSON and HTML output discovery

- JSON/HTML outputs should be written to a predictable report directory chosen by the smoke-run command.
- Capture the generated file paths in the smoke-run runbook before ingestion work begins.

## .NET build verification

- Verify the cBot project builds with the local .NET SDK before smoke backtests.
- Record the exact build command and expected successful output in the smoke-run runbook.
