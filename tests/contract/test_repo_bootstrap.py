from pathlib import Path


def test_repo_bootstrap_layout_exists() -> None:
    required = [
        Path("apps/orchestrator"),
        Path("libs/contracts"),
        Path("tests/contract"),
        Path("scripts/dev"),
    ]
    assert all(path.exists() for path in required)
