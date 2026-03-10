from __future__ import annotations

from libs.contracts.operator_workflow import (
    ReviewChecklist,
    ReviewChecklistItem,
    SafeStrategyConfig,
)


def build_review_checklist(
    *, strategy_summary: str, safe_config: dict[str, object]
) -> ReviewChecklist:
    _ = strategy_summary
    _validated_config = SafeStrategyConfig.model_validate(safe_config)

    labels = (
        "entry rule understood",
        "exit rule understood",
        "symbol confirmed",
        "timeframe confirmed",
        "session confirmed",
        "risk per trade confirmed",
        "stop/take-profit confirmed",
        "overtrading risk reviewed",
        "ready for backtest confirmed",
    )
    items = tuple(ReviewChecklistItem(label=label, completed=False) for label in labels)
    return ReviewChecklist(items=items, is_complete=False)


def can_run_backtest(checklist: ReviewChecklist) -> bool:
    return checklist.is_complete
