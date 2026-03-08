from __future__ import annotations

from datetime import datetime
from importlib import import_module
from typing import Callable, Protocol, cast

from libs.contracts.ledger_event import ArtifactRef, LedgerEvent


class ParsedBacktestReportLike(Protocol):
    run_id: str
    strategy_id: str
    symbol: str
    start_time_utc: datetime
    end_time_utc: datetime
    metrics: dict[str, float]
    report_path: str


parser_module = import_module("libs.ctrader_reports.backtest_parser")
parse_backtest_report = cast(
    Callable[[dict[str, object]], ParsedBacktestReportLike],
    parser_module.parse_backtest_report,
)


def ingest_backtest_report(payload: dict[str, object]) -> list[LedgerEvent]:
    parsed = parse_backtest_report(payload)
    artifact_ref = ArtifactRef(
        kind="report_json",
        path=parsed.report_path,
        content_type="application/json",
        source_system="ctrader_cli",
        sha256="fixture-placeholder",
    )

    return [
        LedgerEvent(
            event_id=f"{parsed.run_id}-started",
            run_id=parsed.run_id,
            source="ctrader_cli",
            event_type="run_started",
            timestamp_utc=parsed.start_time_utc,
            payload={
                "strategy_id": parsed.strategy_id,
                "symbol": parsed.symbol,
            },
            approval_state="not_required",
        ),
        LedgerEvent(
            event_id=f"{parsed.run_id}-metrics",
            run_id=parsed.run_id,
            source="ctrader_cli",
            event_type="metrics_recorded",
            timestamp_utc=parsed.end_time_utc,
            payload=dict(parsed.metrics),
            approval_state="not_required",
            artifact_ref=artifact_ref,
        ),
        LedgerEvent(
            event_id=f"{parsed.run_id}-completed",
            run_id=parsed.run_id,
            source="ctrader_cli",
            event_type="run_completed",
            timestamp_utc=parsed.end_time_utc,
            payload={
                "strategy_id": parsed.strategy_id,
                "symbol": parsed.symbol,
            },
            approval_state="not_required",
        ),
    ]
