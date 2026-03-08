import json
from importlib import import_module
from pathlib import Path
from typing import Callable, Protocol, cast


class PortfolioMetricsLike(Protocol):
    sharpe_ratio: float
    max_drawdown: float
    correlation_matrix: dict[str, dict[str, float]]


analytics_module = import_module("apps.analytics.metrics")
compute_portfolio_metrics = cast(
    Callable[[list[dict[str, object]]], PortfolioMetricsLike],
    analytics_module.compute_portfolio_metrics,
)


def load_payload(path: str) -> list[dict[str, object]]:
    return cast(list[dict[str, object]], json.loads(Path(path).read_text()))


def test_compute_portfolio_metrics_returns_sharpe_drawdown_and_correlation() -> None:
    portfolio_events = load_payload("tests/fixtures/events/portfolio_sample.json")

    metrics = compute_portfolio_metrics(portfolio_events)

    assert metrics.sharpe_ratio is not None
    assert metrics.max_drawdown is not None
    assert metrics.correlation_matrix is not None
