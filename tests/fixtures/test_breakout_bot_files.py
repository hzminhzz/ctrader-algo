from pathlib import Path


def test_breakout_bot_files_exist() -> None:
    assert Path("ctrader/bots/BreakoutBot/BreakoutBot.cs").exists()
    assert Path("ctrader/bots/BreakoutBot/Parameters/smoke.cbotset").exists()


def test_breakout_bot_declares_headless_safe_parameters() -> None:
    source = Path("ctrader/bots/BreakoutBot/BreakoutBot.cs").read_text()
    assert "RiskPerTrade" in source
    assert "StopLoss" in source
