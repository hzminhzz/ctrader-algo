from __future__ import annotations

from pathlib import Path

from apps.operator_ui.workflow import prepare_backtest_request, summarize_run_evaluation


def test_prepare_backtest_request_writes_manifest_and_returns_command(
    tmp_path: Path,
) -> None:
    result = prepare_backtest_request(
        manifest_path=tmp_path / "operator-manifest.json",
        strategy_id="london-breakout",
        safe_config={
            "symbol": "EURUSD",
            "timeframe": "H1",
            "risk_per_trade": 0.01,
            "session_filter": "London",
            "promotion_target": "paper",
        },
    )

    assert result.manifest_path.exists()
    assert "backtest" in result.command
    assert "operator-manifest.json" in result.command


def test_summarize_run_evaluation_returns_operator_facing_sections() -> None:
    summary = summarize_run_evaluation(
        report_payload_path=Path("tests/fixtures/reports/sample_backtest.json"),
        portfolio_events_path=Path("tests/fixtures/events/portfolio_sample.json"),
        prop_rule_events_path=Path("tests/fixtures/events/prop_rule_sample.json"),
        completed_event_path=Path("tests/fixtures/events/sample_ledger_event.json"),
    )

    assert summary["run_id"] == "run-001"
    assert "metrics_recorded" in summary["event_types"]
    assert "journal_summary" in summary
    assert "promotion_status" in summary
