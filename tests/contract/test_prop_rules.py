import json
from importlib import import_module
from pathlib import Path
from typing import Callable, Protocol, cast


class PropStatusLike(Protocol):
    daily_loss_breached: bool


prop_module = import_module("apps.prop_simulator.evaluator")
evaluate_prop_status = cast(
    Callable[[dict[str, object]], PropStatusLike],
    prop_module.evaluate_prop_status,
)


def load_payload(path: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads(Path(path).read_text()))


def test_evaluate_prop_status_flags_daily_loss_breach() -> None:
    prop_rule_events = load_payload("tests/fixtures/events/prop_rule_sample.json")

    result = evaluate_prop_status(prop_rule_events)

    assert result.daily_loss_breached is True
