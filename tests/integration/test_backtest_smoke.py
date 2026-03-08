import json
from pathlib import Path


def test_breakout_bot_algo_package_exists() -> None:
    assert Path("ctrader/cli/runtime/bots.algo").exists()


def test_runtime_backtest_artifacts_exist() -> None:
    assert Path("ctrader/cli/runtime/report.html").exists()
    assert Path("ctrader/cli/runtime/report.json").exists()


def test_sample_backtest_fixture_contains_run_id() -> None:
    payload = json.loads(
        Path("tests/fixtures/reports/sample_backtest.json").read_text()
    )
    assert payload["run_id"]


def test_sample_backtest_fixture_contains_minimum_report_shape() -> None:
    payload = json.loads(
        Path("tests/fixtures/reports/sample_backtest.json").read_text()
    )
    assert payload["strategy_id"]
    assert payload["symbol"]
    assert payload["start_time_utc"]
    assert payload["end_time_utc"]
