from importlib import import_module
from typing import Callable, Protocol, cast


class OpenApiClientLike(Protocol):
    def list_accounts(self) -> list[dict[str, object]]: ...

    def list_positions(self) -> list[dict[str, object]]: ...


open_api_module = import_module("apps.orchestrator.open_api_client")
OpenApiClient = cast(Callable[[], OpenApiClientLike], open_api_module.OpenApiClient)


def test_open_api_client_exposes_account_and_position_methods() -> None:
    client = OpenApiClient()
    assert hasattr(client, "list_accounts")
    assert hasattr(client, "list_positions")
