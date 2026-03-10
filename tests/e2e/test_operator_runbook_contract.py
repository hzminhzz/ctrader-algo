from pathlib import Path


def test_operator_runbook_declares_required_sections() -> None:
    content = Path("docs/runbooks/operator-lifecycle-guide.md").read_text()
    assert "Create" in content
    assert "Review" in content
    assert "Backtest" in content
    assert "Evaluate" in content
    assert "Promote" in content
