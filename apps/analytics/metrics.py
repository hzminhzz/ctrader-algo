from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import TypedDict


class PortfolioEvent(TypedDict):
    run_id: str
    pnl: float
    strategy_id: str


@dataclass(frozen=True)
class PortfolioMetrics:
    sharpe_ratio: float
    max_drawdown: float
    correlation_matrix: dict[str, dict[str, float]]


def compute_portfolio_metrics(
    portfolio_events: list[PortfolioEvent],
) -> PortfolioMetrics:
    pnls = [float(event["pnl"]) for event in portfolio_events]
    average = mean(pnls)
    deviation = pstdev(pnls) if len(pnls) > 1 else 0.0
    sharpe_ratio = average / deviation if deviation else 0.0

    running = 0.0
    peak = 0.0
    max_drawdown = 0.0
    for pnl in pnls:
        running += pnl
        peak = max(peak, running)
        max_drawdown = max(max_drawdown, peak - running)

    strategies = sorted({str(event["strategy_id"]) for event in portfolio_events})
    correlation_matrix = {
        left: {right: 1.0 if left == right else 0.0 for right in strategies}
        for left in strategies
    }

    return PortfolioMetrics(
        sharpe_ratio=sharpe_ratio,
        max_drawdown=max_drawdown,
        correlation_matrix=correlation_matrix,
    )
