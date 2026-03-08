from typing import Final, Literal

APPROVAL_STATES: Final[tuple[str, ...]] = (
    "not_required",
    "pending",
    "approved",
    "rejected",
)

APPROVAL_STATE_OWNERSHIP_RULE: Final[str] = (
    "downstream modules must import these enums and constants rather than re-declare them locally"
)

APPROVAL_STATE_TRANSITIONS: Final[dict[str, tuple[str, ...]]] = {
    "not_required": (),
    "pending": ("approved", "rejected"),
    "approved": (),
    "rejected": (),
}

PROMOTION_TRANSITIONS: Final[dict[str, tuple[str, ...]]] = {
    "approval_granted": ("paper_promotion_requested", "live_promotion_requested"),
    "approval_rejected": (),
}

ApprovalState = Literal["not_required", "pending", "approved", "rejected"]
