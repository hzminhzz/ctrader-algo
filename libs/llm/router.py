from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoutedCommand:
    classification: str
    retry_allowed: bool


def classify_action(action: str) -> RoutedCommand:
    if action == "generate_strategy_draft":
        return RoutedCommand(
            classification="internal_state_mutation_allowed", retry_allowed=True
        )

    if action in {"summarize_results", "draft_discord_message", "draft_tweet"}:
        return RoutedCommand(classification="advisory_only", retry_allowed=True)

    if action in {"propose_strategy_change", "propose_parameter_sweep"}:
        return RoutedCommand(
            classification="internal_state_mutation_allowed", retry_allowed=True
        )

    return RoutedCommand(
        classification="never_directly_executable_against_paper_live",
        retry_allowed=False,
    )
