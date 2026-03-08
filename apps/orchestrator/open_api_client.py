from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OpenApiClient:
    base_url: str = "https://openapi.ctrader.com"

    def list_accounts(self) -> list[dict[str, object]]:
        return []

    def list_positions(self) -> list[dict[str, object]]:
        return []
