import json
from importlib import import_module
from pathlib import Path
from typing import Callable, Protocol, cast


class ParsedBacktestReportLike(Protocol):
    metrics: dict[str, float]


parser_module = import_module("libs.ctrader_reports.backtest_parser")
parse_backtest_report = cast(
    Callable[[dict[str, object]], ParsedBacktestReportLike],
    parser_module.parse_backtest_report,
)


def load_payload(path: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads(Path(path).read_text()))


def test_parse_backtest_report_returns_metrics_dict() -> None:
    sample_backtest_payload = load_payload(
        "tests/fixtures/reports/sample_backtest.json"
    )

    report = parse_backtest_report(sample_backtest_payload)

    assert "net_profit" in report.metrics
