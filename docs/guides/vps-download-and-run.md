# VPS Download and Run Guide

This guide shows how to clone this repository onto a VPS or new machine and run the verified cTrader workflow.

## 1. Clone the repository

```bash
git clone https://github.com/hzminhzz/ctrader-algo.git
cd ctrader-algo
```

## 2. Install prerequisites

You need:

- Python 3.12+
- .NET SDK
- Docker Desktop or Docker Engine

Check them:

```bash
python --version
dotnet --version
docker --version
docker ps
```

## 3. Build the cBot into a `.algo`

```bash
dotnet build ctrader/bots/BreakoutBot/BreakoutBot.csproj -c Release
```

Expected result:

- `.algo` is published to your cTrader robot sources path
- the repo-local runtime copy should be staged to `ctrader/cli/runtime/bots.algo`

If needed, copy it manually:

```bash
mkdir -p ctrader/cli/runtime
cp ~/cAlgo/Sources/Robots/bots.algo ctrader/cli/runtime/bots.algo
```

## 4. Prepare credentials for backtesting

Create the password file used by `ctrader-console`:

```bash
printf '%s\n' 'YOUR_PASSWORD' > ctrader/cli/runtime/ctid-password.txt
```

Do not commit this file.

## 5. Run the verified Docker metadata command

```bash
docker run --rm --platform linux/amd64 \
  --mount type=bind,src="$(pwd)/ctrader/cli/runtime",dst=/mnt/algo \
  ghcr.io/spotware/ctrader-console:latest \
  metadata "/mnt/algo/bots.algo"
```

This confirms the `.algo` package is readable.

## 6. Run the verified Docker backtest command

```bash
docker run --rm --platform linux/amd64 \
  --mount type=bind,src="$(pwd)/ctrader/cli/runtime",dst=/mnt/algo \
  -e CTID='YOUR_CTID' \
  -e PWD-FILE='/mnt/algo/ctid-password.txt' \
  -e ACCOUNT='YOUR_ACCOUNT' \
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

Expected output files:

- `ctrader/cli/runtime/report.html`
- `ctrader/cli/runtime/report.json`

## 7. Verify the repository logic

```bash
python -m pytest tests/contract -v
python -m pytest tests/integration -v
python -m pytest tests/e2e -v
python -m pytest tests/fixtures -v
bash scripts/ci/smoke.sh
```

## 8. Example operator workflow

Use this daily sequence:

1. modify or add a cBot idea
2. build `.algo`
3. run Docker backtest
4. inspect `report.json`
5. ingest/evaluate through the repo modules
6. review prop-rule and workflow gate results
7. only then trigger Discord or tweet draft outputs

## 9. Important files

- `docs/runbooks/ctrader-backtest-smoke.md`
- `docs/runbooks/ctrader-cli-environment.md`
- `docs/runbooks/promotion-gates.md`
- `docs/runbooks/desktop-automation-boundaries.md`
