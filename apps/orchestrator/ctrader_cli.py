from __future__ import annotations


def build_backtest_command(manifest_path: str, mode: str = "backtest") -> list[str]:
    if mode != "backtest":
        raise ValueError("unsupported mode")

    return ["ctrader", "backtest", "--manifest", manifest_path]
