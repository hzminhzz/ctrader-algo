from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderRequest:
    action: str
    schema_version: str


@dataclass(frozen=True)
class ProviderResponse:
    action: str
    schema_version: str
    raw_payload: dict[str, object]
