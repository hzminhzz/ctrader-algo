from importlib import import_module
from typing import Callable, cast


ctrader_cli = import_module("apps.orchestrator.ctrader_cli")
build_backtest_command = cast(
    Callable[..., list[str]], ctrader_cli.build_backtest_command
)


def test_build_backtest_command_contains_required_flags() -> None:
    command = build_backtest_command("manifest.json")
    assert "backtest" in command
    assert "manifest.json" in command


def test_build_backtest_command_rejects_unsupported_optimization_flags() -> None:
    try:
        _ = build_backtest_command("manifest.json", mode="optimize")
    except ValueError:
        assert True
    else:
        assert False
