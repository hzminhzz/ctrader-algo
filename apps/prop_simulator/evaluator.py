from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

from .rules import STARTER_PROP_PACK


class PropRuleEvent(TypedDict):
    rule_pack: str
    daily_pnl: float
    daily_loss_limit: float
    trailing_drawdown: float
    trailing_drawdown_limit: float
    open_positions: int
    max_positions: int
    within_trading_window: bool


@dataclass(frozen=True)
class PropStatus:
    daily_loss_breached: bool
    trailing_drawdown_breached: bool
    max_positions_breached: bool
    trading_window_breached: bool


def evaluate_prop_status(prop_rule_events: PropRuleEvent) -> PropStatus:
    daily_pnl = float(prop_rule_events["daily_pnl"])
    trailing_drawdown = float(prop_rule_events["trailing_drawdown"])
    open_positions = int(prop_rule_events["open_positions"])
    within_trading_window = bool(prop_rule_events["within_trading_window"])

    return PropStatus(
        daily_loss_breached=abs(daily_pnl) > STARTER_PROP_PACK.daily_loss_limit,
        trailing_drawdown_breached=trailing_drawdown
        > STARTER_PROP_PACK.trailing_drawdown_limit,
        max_positions_breached=open_positions > STARTER_PROP_PACK.max_positions,
        trading_window_breached=not within_trading_window,
    )
