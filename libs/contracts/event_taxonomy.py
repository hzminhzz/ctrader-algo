from typing import Final, Literal

EVENT_TYPES: Final[tuple[str, ...]] = (
    "run_requested",
    "run_started",
    "run_completed",
    "run_failed",
    "metrics_recorded",
    "approval_requested",
    "approval_granted",
    "approval_rejected",
    "paper_promotion_requested",
    "live_promotion_requested",
    "discord_draft_created",
    "tweet_draft_created",
)

TAXONOMY_OWNERSHIP_RULE: Final[str] = (
    "downstream modules must import these enums and constants rather than re-declare them locally"
)

ARTIFACT_REF_FIELDS: Final[tuple[str, ...]] = (
    "kind",
    "path",
    "content_type",
    "source_system",
    "sha256",
)

EventType = Literal[
    "run_requested",
    "run_started",
    "run_completed",
    "run_failed",
    "metrics_recorded",
    "approval_requested",
    "approval_granted",
    "approval_rejected",
    "paper_promotion_requested",
    "live_promotion_requested",
    "discord_draft_created",
    "tweet_draft_created",
]
