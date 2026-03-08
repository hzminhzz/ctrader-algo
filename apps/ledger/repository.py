from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LedgerRepository:
    events: list[dict[str, object]] = field(default_factory=list)

    def append(self, event: dict[str, object]) -> None:
        self.events.append(event)

    def list_by_run_id(self, run_id: str) -> list[dict[str, object]]:
        return [event for event in self.events if event.get("run_id") == run_id]
