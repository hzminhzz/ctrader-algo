import json
from importlib import import_module
from pathlib import Path
from typing import Callable, Protocol, cast


class JournalEntryLike(Protocol):
    summary: str


journal_module = import_module("apps.journal.projections")
build_journal_entry = cast(
    Callable[[dict[str, object]], JournalEntryLike],
    journal_module.build_journal_entry,
)


def load_event(path: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads(Path(path).read_text()))


def test_build_journal_entry_contains_trade_summary() -> None:
    backtest_completed_event = load_event(
        "tests/fixtures/events/sample_ledger_event.json"
    )

    entry = build_journal_entry(backtest_completed_event)

    assert entry.summary
