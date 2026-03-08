import json
from importlib import import_module
from pathlib import Path
from typing import Callable, Protocol, cast


class ValidationResultLike(Protocol):
    is_valid: bool


llm_validator = import_module("libs.llm.validator")
validate_command = cast(
    Callable[[dict[str, object]], ValidationResultLike],
    llm_validator.validate_command,
)


def load_payload(path: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads(Path(path).read_text()))


def test_validate_command_rejects_unknown_action() -> None:
    invalid_command_payload = load_payload("tests/fixtures/llm/invalid_command.json")

    result = validate_command(invalid_command_payload)

    assert result.is_valid is False
