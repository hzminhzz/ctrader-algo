from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PropRulePack:
    name: str
    daily_loss_limit: float
    trailing_drawdown_limit: float
    max_positions: int


STARTER_PROP_PACK = PropRulePack(
    name="starter_prop_pack",
    daily_loss_limit=500.0,
    trailing_drawdown_limit=1000.0,
    max_positions=3,
)
