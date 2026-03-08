import json
from importlib import import_module
from pathlib import Path
from typing import Callable, Protocol, cast


class ArtifactRefLike(Protocol):
    path: str


class LedgerEventLike(Protocol):
    event_type: str

    @property
    def artifact_ref(self) -> object: ...


ledger_module = import_module("apps.ledger.ingest_backtest")
ingest_backtest_report = cast(
    Callable[[dict[str, object]], list[LedgerEventLike]],
    ledger_module.ingest_backtest_report,
)


def load_payload(path: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads(Path(path).read_text()))


def test_backtest_ingest_emits_run_and_metrics_events() -> None:
    sample_backtest_payload = load_payload(
        "tests/fixtures/reports/sample_backtest.json"
    )

    events = ingest_backtest_report(sample_backtest_payload)

    event_types = [event.event_type for event in events]
    assert "run_started" in event_types
    assert "run_completed" in event_types
    assert "metrics_recorded" in event_types

    artifact_event = next(
        event for event in events if event.event_type == "metrics_recorded"
    )
    artifact_ref = cast(ArtifactRefLike, artifact_event.artifact_ref)
    assert artifact_ref is not None
    assert artifact_ref.path == "ctrader/cli/runtime/report.json"
