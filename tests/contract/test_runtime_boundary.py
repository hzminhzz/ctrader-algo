from importlib import import_module
from typing import cast


runtime_boundary = import_module("libs.risk.runtime_boundary")
BOT_ENFORCED_CONTROLS = cast(tuple[str, ...], runtime_boundary.BOT_ENFORCED_CONTROLS)
EXTERNAL_ONLY_CAPABILITIES = cast(
    tuple[str, ...], runtime_boundary.EXTERNAL_ONLY_CAPABILITIES
)


def test_runtime_boundary_separates_execution_risk_from_external_services() -> None:
    assert "max_open_risk" in BOT_ENFORCED_CONTROLS
    assert "tweet_publish" in EXTERNAL_ONLY_CAPABILITIES


def test_runtime_boundary_matches_planned_control_sets() -> None:
    assert BOT_ENFORCED_CONTROLS == (
        "sizing",
        "stop_loss_placement",
        "max_open_risk",
        "trading_window_checks",
        "instrument_allowlist",
        "kill_switch_hooks",
    )
    assert EXTERNAL_ONLY_CAPABILITIES == (
        "llm_reasoning",
        "analytics",
        "journal_views",
        "discord_messaging",
        "tweet_drafting",
        "approvals",
        "simulator_projections",
        "tweet_publish",
    )
