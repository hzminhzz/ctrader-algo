from typing import Literal, cast, get_args

import pytest
from pydantic import ValidationError

from libs.contracts.llm_commands import LlmAction, LlmCommand


def test_llm_command_requires_action_and_schema_version() -> None:
    with pytest.raises(ValidationError):
        _ = LlmCommand.model_validate({})


def test_llm_command_rejects_unknown_action() -> None:
    with pytest.raises(ValidationError):
        _ = LlmCommand.model_validate(
            {
                "action": "trade_live_now",
                "schema_version": "1.0",
            }
        )


def test_llm_command_accepts_allowed_action() -> None:
    allowed_actions = cast(
        tuple[
            Literal[
                "propose_strategy_change",
                "propose_parameter_sweep",
                "summarize_results",
                "draft_discord_message",
                "draft_tweet",
            ],
            ...,
        ],
        get_args(LlmAction),
    )

    for action in allowed_actions:
        command = LlmCommand.model_validate(
            {
                "action": action,
                "schema_version": "1.0",
            }
        )

        assert command.action == action


def test_llm_command_rejects_unknown_schema_version() -> None:
    with pytest.raises(ValidationError):
        _ = LlmCommand.model_validate(
            {
                "action": "summarize_results",
                "schema_version": "2.0",
            }
        )


def test_llm_command_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        _ = LlmCommand.model_validate(
            {
                "action": "summarize_results",
                "schema_version": "1.0",
                "unexpected": True,
            }
        )


def test_llm_command_is_immutable() -> None:
    command = LlmCommand.model_validate(
        {
            "action": "summarize_results",
            "schema_version": "1.0",
        }
    )

    with pytest.raises(ValidationError):
        command.action = "draft_tweet"
