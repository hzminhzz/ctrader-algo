from __future__ import annotations

from typing import get_args

import pytest
from pydantic import ValidationError

from libs.contracts.operator_workflow import (
    OperatorStage,
    ReviewChecklist,
    SafeStrategyConfig,
    StrategyBrief,
    StrategyDraft,
)


def test_strategy_brief_requires_plain_language_goal() -> None:
    with pytest.raises(ValidationError):
        StrategyBrief.model_validate({})


def test_safe_strategy_config_accepts_expected_fields() -> None:
    config = SafeStrategyConfig.model_validate(
        {
            "symbol": "EURUSD",
            "timeframe": "H1",
            "risk_per_trade": 0.01,
            "session_filter": "London",
            "promotion_target": "paper",
        }
    )

    assert config.symbol == "EURUSD"
    assert config.timeframe == "H1"


def test_strategy_draft_and_review_checklist_have_minimum_shape() -> None:
    draft = StrategyDraft.model_validate(
        {
            "strategy_id": "london-breakout",
            "plain_english_summary": "Trade EURUSD H1 London breakouts.",
            "generated_code": "// generated cBot draft placeholder",
            "review_status": "pending",
        }
    )
    checklist = ReviewChecklist.model_validate(
        {
            "items": [
                {
                    "label": "entry rule understood",
                    "completed": False,
                }
            ],
            "is_complete": False,
        }
    )

    assert draft.review_status == "pending"
    assert checklist.is_complete is False


def test_operator_stage_literal_contains_expected_values() -> None:
    assert get_args(OperatorStage) == (
        "create",
        "review",
        "backtest_ready",
        "backtest_running",
        "evaluate",
        "promote",
    )
