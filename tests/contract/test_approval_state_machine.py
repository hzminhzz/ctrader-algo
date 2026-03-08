from libs.contracts.approval_states import (
    APPROVAL_STATES,
    APPROVAL_STATE_TRANSITIONS,
    APPROVAL_STATE_OWNERSHIP_RULE,
    PROMOTION_TRANSITIONS,
)


def test_approval_state_machine_allows_expected_review_flow() -> None:
    assert APPROVAL_STATE_TRANSITIONS["pending"] == ("approved", "rejected")


def test_promotion_transitions_require_approval_before_live() -> None:
    assert PROMOTION_TRANSITIONS["approval_granted"] == (
        "paper_promotion_requested",
        "live_promotion_requested",
    )


def test_approval_states_match_full_contract() -> None:
    assert APPROVAL_STATES == ("not_required", "pending", "approved", "rejected")
    assert APPROVAL_STATE_TRANSITIONS == {
        "not_required": (),
        "pending": ("approved", "rejected"),
        "approved": (),
        "rejected": (),
    }


def test_approval_state_module_declares_shared_ownership_rule() -> None:
    assert (
        APPROVAL_STATE_OWNERSHIP_RULE
        == "downstream modules must import these enums and constants rather than re-declare them locally"
    )
