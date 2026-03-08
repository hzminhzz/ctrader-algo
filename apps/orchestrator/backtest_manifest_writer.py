from __future__ import annotations

from pathlib import Path

from libs.contracts.backtest_manifest import BacktestManifest


def write_manifest(destination: Path) -> None:
    manifest = BacktestManifest.model_validate(
        {
            "strategy_id": "breakout-bot",
            "symbol": "EURUSD",
            "timeframe": "H1",
            "start": "2025-01-01T00:00:00Z",
            "end": "2025-01-31T00:00:00Z",
            "starting_balance": 10000,
            "spread_mode": "fixed",
            "commission_mode": "per_lot",
            "parameter_set_path": "ctrader/bots/BreakoutBot/Parameters/smoke.cbotset",
            "output_path": str(destination),
            "run_id": "run-001",
        }
    )

    destination.parent.mkdir(parents=True, exist_ok=True)
    _ = destination.write_text(manifest.model_dump_json(indent=2))
