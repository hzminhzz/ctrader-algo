# cTrader Backtest Smoke Runbook

## Verified prerequisites

- Docker Desktop running on macOS.
- Official image: `ghcr.io/spotware/ctrader-console:latest`.
- Built `.algo` package present at `ctrader/cli/runtime/bots.algo`.
- Password file path expected inside mounted runtime directory.

## Verified metadata command

```bash
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
docker run --rm --platform linux/amd64 \
  --mount type=bind,src="$(pwd)/ctrader/cli/runtime",dst=/mnt/algo \
  ghcr.io/spotware/ctrader-console:latest \
  metadata "/mnt/algo/bots.algo"
```

This command successfully reads the built `.algo` and prints bot metadata.

## Verified backtest command shape

```bash
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
docker run --rm --platform linux/amd64 \
  --mount type=bind,src="$(pwd)/ctrader/cli/runtime",dst=/mnt/algo \
  -e CTID='<your-ctid>' \
  -e PWD-FILE='/mnt/algo/ctid-password.txt' \
  -e ACCOUNT='<your-account-id>' \
  -e SYMBOL='EURUSD' \
  -e PERIOD='H1' \
  -e START='01/01/2025' \
  -e END='31/01/2025' \
  -e DATA-MODE='m1' \
  -e BALANCE='10000' \
  -e COMMISSION='30' \
  -e SPREAD='1' \
  -e REPORT='/mnt/algo/report.html' \
  -e REPORT-JSON='/mnt/algo/report.json' \
  ghcr.io/spotware/ctrader-console:latest \
  backtest "/mnt/algo/bots.algo" --environment-variables --exit-on-stop
```

## Verified successful backtest run

The Docker backtest command now runs successfully with a valid cTrader ID, account, and password file. Verified runtime behavior:

- container connected and logged in successfully
- backtest loaded `EURUSD` on `H1`
- bot started and stopped cleanly
- output artifacts were written to the mounted runtime directory

Observed summary from the successful run:

```text
Equity: 10000
NetProfit: 0
WinningTrades: 0
LosingTrades: 0
TotalTrades: 0
Fitness: 0
```

## Expected output files on success

- `ctrader/cli/runtime/report.html`
- `ctrader/cli/runtime/report.json`

## Captured output files

- `ctrader/cli/runtime/report.html`
- `ctrader/cli/runtime/report.json`
- `tests/fixtures/reports/sample_backtest.json` (sanitized representative fixture derived from the successful run)
