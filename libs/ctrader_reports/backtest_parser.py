from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict


class MetricsPayload(TypedDict):
    net_profit: float
    max_drawdown: float
    win_rate: float


class ArtifactsPayload(TypedDict):
    report_json: str


class BacktestReportPayload(TypedDict):
    run_id: str
    strategy_id: str
    symbol: str
    start_time_utc: str
    end_time_utc: str
    metrics: MetricsPayload
    artifacts: ArtifactsPayload


@dataclass(frozen=True)
class ParsedBacktestReport:
    run_id: str
    strategy_id: str
    symbol: str
    start_time_utc: datetime
    end_time_utc: datetime
    metrics: dict[str, float]
    report_path: str


def parse_utc_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_backtest_report(payload: BacktestReportPayload) -> ParsedBacktestReport:
    metrics = payload["metrics"]
    artifacts = payload["artifacts"]

    return ParsedBacktestReport(
        run_id=payload["run_id"],
        strategy_id=payload["strategy_id"],
        symbol=payload["symbol"],
        start_time_utc=parse_utc_timestamp(payload["start_time_utc"]),
        end_time_utc=parse_utc_timestamp(payload["end_time_utc"]),
        metrics={
            "net_profit": float(metrics["net_profit"]),
            "max_drawdown": float(metrics["max_drawdown"]),
            "win_rate": float(metrics["win_rate"]),
        },
        report_path=artifacts["report_json"],
    )
