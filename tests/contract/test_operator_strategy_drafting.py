from __future__ import annotations

from apps.operator_ui.drafting import generate_strategy_draft


def test_generate_strategy_draft_returns_plain_summary_and_code() -> None:
    draft = generate_strategy_draft(
        brief={
            "title": "London breakout",
            "goal": "Trade London breakout moves",
            "entry_idea": "Buy breakout above range high",
            "exit_idea": "Exit at stop loss or take profit",
            "risk_notes": "Use 1 percent risk",
        },
        safe_config={
            "symbol": "EURUSD",
            "timeframe": "H1",
            "risk_per_trade": 0.01,
            "session_filter": "London",
            "promotion_target": "paper",
        },
    )

    assert draft.strategy_id == "london-breakout"
    assert draft.plain_english_summary
    assert draft.generated_code
    assert draft.review_status == "pending"
