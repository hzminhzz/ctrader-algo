from libs.contracts.event_taxonomy import (
    ARTIFACT_REF_FIELDS,
    EVENT_TYPES,
    TAXONOMY_OWNERSHIP_RULE,
)


def test_event_taxonomy_contains_required_promotion_events() -> None:
    assert "approval_requested" in EVENT_TYPES
    assert "live_promotion_requested" in EVENT_TYPES


def test_event_taxonomy_contains_required_artifact_fields() -> None:
    assert ARTIFACT_REF_FIELDS == (
        "kind",
        "path",
        "content_type",
        "source_system",
        "sha256",
    )


def test_event_taxonomy_matches_full_contract() -> None:
    assert EVENT_TYPES == (
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


def test_event_taxonomy_declares_shared_ownership_rule() -> None:
    assert (
        TAXONOMY_OWNERSHIP_RULE
        == "downstream modules must import these enums and constants rather than re-declare them locally"
    )
