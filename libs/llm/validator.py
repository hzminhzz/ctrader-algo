from __future__ import annotations

from dataclasses import dataclass

from libs.contracts.llm_commands import LlmCommand

from .router import RoutedCommand, classify_action


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    reason: str | None
    classification: str
    retry_allowed: bool


def validate_command(payload: dict[str, object]) -> ValidationResult:
    try:
        command = LlmCommand.model_validate(payload)
    except Exception:
        routed: RoutedCommand = classify_action(str(payload.get("action", "")))
        return ValidationResult(
            is_valid=False,
            reason="invalid_command_payload",
            classification=routed.classification,
            retry_allowed=routed.retry_allowed,
        )

    routed = classify_action(command.action)
    return ValidationResult(
        is_valid=True,
        reason=None,
        classification=routed.classification,
        retry_allowed=routed.retry_allowed,
    )
