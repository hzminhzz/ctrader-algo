from pathlib import Path


def test_smoke_script_exists() -> None:
    assert Path("scripts/ci/smoke.sh").exists()


def test_smoke_script_declares_contract_and_integration_runs() -> None:
    content = Path("scripts/ci/smoke.sh").read_text()
    assert "tests/contract" in content
    assert "tests/integration" in content


def test_runbooks_exist_for_promotion_and_desktop_boundaries() -> None:
    assert Path("docs/runbooks/promotion-gates.md").exists()
    assert Path("docs/runbooks/desktop-automation-boundaries.md").exists()


def test_promotion_runbook_mentions_human_approval_for_paper_and_live() -> None:
    content = Path("docs/runbooks/promotion-gates.md").read_text()
    assert "paper" in content
    assert "live" in content
    assert "approval" in content
