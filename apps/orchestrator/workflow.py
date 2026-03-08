from __future__ import annotations


def requires_approval(stage: str) -> bool:
    return stage in {"simulator_passed", "paper_eligible", "live_eligible"}


def next_stage(current_stage: str, approved: bool) -> str:
    if current_stage == "simulator_passed" and requires_approval(current_stage):
        return "paper_eligible" if approved else "awaiting_approval"

    if current_stage == "paper_eligible":
        return "live_eligible" if approved else "awaiting_approval"

    return current_stage
