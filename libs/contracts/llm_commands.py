from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict

LlmAction = Literal[
    "generate_strategy_draft",
    "propose_strategy_change",
    "propose_parameter_sweep",
    "summarize_results",
    "draft_discord_message",
    "draft_tweet",
]
SchemaVersion = Literal["1.0"]


class LlmCommand(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    action: LlmAction
    schema_version: SchemaVersion
