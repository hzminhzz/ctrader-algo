from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Annotated, ClassVar, cast

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from libs.contracts.approval_states import ApprovalState
from libs.contracts.event_taxonomy import EventType

UtcTimestamp = Annotated[datetime, Field()]
NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


def freeze_mapping(value: Mapping[str, object]) -> Mapping[str, object]:
    frozen_dict: dict[str, object] = {}
    for key, nested in value.items():
        frozen_dict[key] = freeze_value(nested)
    return MappingProxyType(frozen_dict)


def freeze_sequence(value: list[object]) -> tuple[object, ...]:
    return tuple(freeze_value(item) for item in value)


def freeze_value(value: object) -> object:
    if isinstance(value, Mapping):
        typed_source = cast(Mapping[str, object], value)
        typed_mapping: dict[str, object] = {}
        for key, nested in typed_source.items():
            typed_mapping[key] = nested
        return freeze_mapping(typed_mapping)
    if isinstance(value, list):
        typed_list = cast(list[object], value)
        return freeze_sequence(typed_list)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    msg = "payload values must be JSON-compatible"
    raise ValueError(msg)


class ArtifactRef(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    kind: NonEmptyStr
    path: NonEmptyStr
    content_type: NonEmptyStr
    source_system: NonEmptyStr
    sha256: NonEmptyStr


class LedgerEvent(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)

    event_id: NonEmptyStr
    run_id: NonEmptyStr
    source: NonEmptyStr
    event_type: EventType
    timestamp_utc: UtcTimestamp
    payload: Mapping[str, object]
    approval_state: ApprovalState
    artifact_ref: ArtifactRef | None = None

    @field_validator("timestamp_utc")
    @classmethod
    def validate_utc_timestamp(cls, value: datetime) -> datetime:
        if value.utcoffset() != timezone.utc.utcoffset(value):
            msg = "timestamp must be UTC"
            raise ValueError(msg)
        return value

    @field_validator("payload")
    @classmethod
    def freeze_payload(cls, value: Mapping[str, object]) -> Mapping[str, object]:
        return freeze_mapping(value)
