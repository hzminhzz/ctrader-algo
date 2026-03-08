from pathlib import Path


def test_ctrader_cli_environment_runbook_declares_required_sections() -> None:
    content = Path("docs/runbooks/ctrader-cli-environment.md").read_text()
    assert "Supported cTrader version" in content
    assert "Runner OS" in content
    assert "Artifact directories" in content
