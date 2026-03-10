from __future__ import annotations

from typing import Annotated, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Timeframe = Literal["M1", "M5", "M15", "M30", "H1", "H4", "D1"]
PromotionTarget = Literal["paper", "live"]
ReviewStatus = Literal["pending", "approved", "rejected"]
OperatorStage = Literal[
    "create",
    "review",
    "backtest_ready",
    "backtest_running",
    "evaluate",
    "promote",
]


class StrategyBrief(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    title: NonEmptyStr
    goal: NonEmptyStr
    entry_idea: NonEmptyStr
    exit_idea: NonEmptyStr
    risk_notes: NonEmptyStr


class SafeStrategyConfig(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    symbol: NonEmptyStr
    timeframe: Timeframe
    risk_per_trade: Annotated[float, Field(gt=0, le=1)]
    session_filter: NonEmptyStr
    stop_loss_pips: Annotated[float, Field(gt=0)] = 20.0
    take_profit_pips: Annotated[float, Field(gt=0)] = 40.0
    promotion_target: PromotionTarget


class StrategyDraft(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    strategy_id: NonEmptyStr
    plain_english_summary: NonEmptyStr
    generated_code: NonEmptyStr
    review_status: ReviewStatus


class ReviewChecklistItem(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    label: NonEmptyStr
    completed: bool


class ReviewChecklist(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    items: tuple[ReviewChecklistItem, ...]
    is_complete: bool
