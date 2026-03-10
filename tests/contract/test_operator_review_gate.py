from __future__ import annotations

from apps.operator_ui.review import build_review_checklist, can_run_backtest


def test_backtest_remains_blocked_until_all_review_items_are_complete() -> None:
    checklist = build_review_checklist(
        strategy_summary="Trade EURUSD H1 breakout during London",
        safe_config={
            "symbol": "EURUSD",
            "timeframe": "H1",
            "risk_per_trade": 0.01,
            "session_filter": "London",
            "promotion_target": "paper",
        },
    )

    assert can_run_backtest(checklist) is False
