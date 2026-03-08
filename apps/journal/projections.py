from __future__ import annotations

from dataclasses import dataclass
from typing import cast


@dataclass(frozen=True)
class JournalEntry:
    summary: str


def build_journal_entry(backtest_completed_event: dict[str, object]) -> JournalEntry:
    payload = cast(dict[str, object], backtest_completed_event.get("payload", {}))
    strategy_id = str(payload.get("strategy_id", "unknown-strategy"))
    symbol = str(payload.get("symbol", "unknown-symbol"))
    run_id = str(backtest_completed_event.get("run_id", "unknown-run"))
    return JournalEntry(summary=f"{strategy_id} completed on {symbol} for {run_id}")
