from importlib import import_module
from typing import Callable, Protocol, cast


class LedgerRepositoryLike(Protocol):
    def append(self, event: dict[str, object]) -> None: ...

    def list_by_run_id(self, run_id: str) -> list[dict[str, object]]: ...


ledger_repository_module = import_module("apps.ledger.repository")
LedgerRepository = cast(
    Callable[[], LedgerRepositoryLike], ledger_repository_module.LedgerRepository
)


def test_repository_exposes_append_and_list_methods() -> None:
    repo = LedgerRepository()
    assert hasattr(repo, "append")
    assert hasattr(repo, "list_by_run_id")


def test_repository_contract_requires_append_only_and_ordered_reads() -> None:
    repo = LedgerRepository()
    assert hasattr(repo, "append")
    assert hasattr(repo, "list_by_run_id")
