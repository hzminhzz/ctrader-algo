from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError

from libs.contracts.backtest_manifest import BacktestManifest


def test_backtest_manifest_requires_symbol_and_dates() -> None:
    with pytest.raises(ValidationError):
        _ = BacktestManifest.model_validate({})


def test_backtest_manifest_requires_symbol_start_and_end() -> None:
    with pytest.raises(ValidationError) as exc_info:
        _ = BacktestManifest.model_validate(
            {
                "strategy_id": "breakout-bot",
                "timeframe": "H1",
                "starting_balance": 10000,
                "spread_mode": "fixed",
                "commission_mode": "per_lot",
                "parameter_set_path": "ctrader/bots/BreakoutBot/Parameters/smoke.cbotset",
                "output_path": "ctrader/fixtures/reports/sample_backtest.json",
                "run_id": "run-001",
            }
        )

    locations = {tuple(error["loc"]) for error in exc_info.value.errors()}
    assert ("symbol",) in locations
    assert ("start",) in locations
    assert ("end",) in locations


def test_backtest_manifest_accepts_valid_payload() -> None:
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
            "output_path": "ctrader/fixtures/reports/sample_backtest.json",
            "run_id": "run-001",
        }
    )

    assert manifest.symbol == "EURUSD"
    assert manifest.timeframe == "H1"


def test_backtest_manifest_accepts_semantic_utc_timezone() -> None:
    manifest = BacktestManifest.model_validate(
        {
            "strategy_id": "breakout-bot",
            "symbol": "EURUSD",
            "timeframe": "H1",
            "start": datetime(2025, 1, 1, tzinfo=ZoneInfo("UTC")),
            "end": datetime(2025, 1, 31, tzinfo=ZoneInfo("UTC")),
            "starting_balance": 10000,
            "spread_mode": "fixed",
            "commission_mode": "per_lot",
            "parameter_set_path": "ctrader/bots/BreakoutBot/Parameters/smoke.cbotset",
            "output_path": "ctrader/fixtures/reports/sample_backtest.json",
            "run_id": "run-001",
        }
    )

    assert manifest.start.utcoffset() is not None


def test_backtest_manifest_rejects_invalid_timeframe() -> None:
    with pytest.raises(ValidationError):
        _ = BacktestManifest.model_validate(
            {
                "strategy_id": "breakout-bot",
                "symbol": "EURUSD",
                "timeframe": "W1",
                "start": "2025-01-01T00:00:00Z",
                "end": "2025-01-31T00:00:00Z",
                "starting_balance": 10000,
                "spread_mode": "fixed",
                "commission_mode": "per_lot",
                "parameter_set_path": "ctrader/bots/BreakoutBot/Parameters/smoke.cbotset",
                "output_path": "ctrader/fixtures/reports/sample_backtest.json",
                "run_id": "run-001",
            }
        )


def test_backtest_manifest_rejects_non_utc_timestamp() -> None:
    with pytest.raises(ValidationError):
        _ = BacktestManifest.model_validate(
            {
                "strategy_id": "breakout-bot",
                "symbol": "EURUSD",
                "timeframe": "H1",
                "start": "2025-01-01T00:00:00+07:00",
                "end": "2025-01-31T00:00:00Z",
                "starting_balance": 10000,
                "spread_mode": "fixed",
                "commission_mode": "per_lot",
                "parameter_set_path": "ctrader/bots/BreakoutBot/Parameters/smoke.cbotset",
                "output_path": "ctrader/fixtures/reports/sample_backtest.json",
                "run_id": "run-001",
            }
        )


def test_backtest_manifest_rejects_invalid_starting_balance() -> None:
    with pytest.raises(ValidationError):
        _ = BacktestManifest.model_validate(
            {
                "strategy_id": "breakout-bot",
                "symbol": "EURUSD",
                "timeframe": "H1",
                "start": "2025-01-01T00:00:00Z",
                "end": "2025-01-31T00:00:00Z",
                "starting_balance": -1,
                "spread_mode": "fixed",
                "commission_mode": "per_lot",
                "parameter_set_path": "ctrader/bots/BreakoutBot/Parameters/smoke.cbotset",
                "output_path": "ctrader/fixtures/reports/sample_backtest.json",
                "run_id": "run-001",
            }
        )


def test_backtest_manifest_rejects_empty_identifiers() -> None:
    with pytest.raises(ValidationError):
        _ = BacktestManifest.model_validate(
            {
                "strategy_id": "",
                "symbol": "   ",
                "timeframe": "H1",
                "start": "2025-01-01T00:00:00Z",
                "end": "2025-01-31T00:00:00Z",
                "starting_balance": 10000,
                "spread_mode": "fixed",
                "commission_mode": "per_lot",
                "parameter_set_path": "ctrader/bots/BreakoutBot/Parameters/smoke.cbotset",
                "output_path": "ctrader/fixtures/reports/sample_backtest.json",
                "run_id": "run-001",
            }
        )


def test_backtest_manifest_rejects_end_before_start() -> None:
    with pytest.raises(ValidationError):
        _ = BacktestManifest.model_validate(
            {
                "strategy_id": "breakout-bot",
                "symbol": "EURUSD",
                "timeframe": "H1",
                "start": "2025-01-31T00:00:00Z",
                "end": "2025-01-01T00:00:00Z",
                "starting_balance": 10000,
                "spread_mode": "fixed",
                "commission_mode": "per_lot",
                "parameter_set_path": "ctrader/bots/BreakoutBot/Parameters/smoke.cbotset",
                "output_path": "ctrader/fixtures/reports/sample_backtest.json",
                "run_id": "run-001",
            }
        )


def test_backtest_manifest_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        _ = BacktestManifest.model_validate(
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
                "output_path": "ctrader/fixtures/reports/sample_backtest.json",
                "run_id": "run-001",
                "unexpected": True,
            }
        )


def test_backtest_manifest_is_immutable() -> None:
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
            "output_path": "ctrader/fixtures/reports/sample_backtest.json",
            "run_id": "run-001",
        }
    )

    with pytest.raises(ValidationError):
        manifest.symbol = "GBPUSD"
