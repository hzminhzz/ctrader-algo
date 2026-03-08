BOT_ENFORCED_CONTROLS = (
    "sizing",
    "stop_loss_placement",
    "max_open_risk",
    "trading_window_checks",
    "instrument_allowlist",
    "kill_switch_hooks",
)

EXTERNAL_ONLY_CAPABILITIES = (
    "llm_reasoning",
    "analytics",
    "journal_views",
    "discord_messaging",
    "tweet_drafting",
    "approvals",
    "simulator_projections",
    "tweet_publish",
)

FORBIDDEN_BEHAVIOR = ("external services must never directly decide live orders",)
