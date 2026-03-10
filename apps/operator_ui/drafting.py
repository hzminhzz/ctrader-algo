from __future__ import annotations

from libs.contracts.operator_workflow import (
    SafeStrategyConfig,
    StrategyBrief,
    StrategyDraft,
)
from libs.llm.validator import validate_command


def slugify_title(title: str) -> str:
    normalized = "-".join(title.lower().strip().split())
    return normalized or "generated-strategy"


def generate_strategy_draft(
    *, brief: dict[str, object], safe_config: dict[str, object]
) -> StrategyDraft:
    validated_brief = StrategyBrief.model_validate(brief)
    validated_config = SafeStrategyConfig.model_validate(safe_config)

    validation = validate_command(
        {
            "action": "generate_strategy_draft",
            "schema_version": "1.0",
        }
    )
    if not validation.is_valid:
        msg = validation.reason or "invalid_strategy_draft_request"
        raise ValueError(msg)

    strategy_id = slugify_title(validated_brief.title)
    summary = (
        f"Trade {validated_config.symbol} {validated_config.timeframe} "
        f"{validated_config.session_filter} setups using {validated_brief.entry_idea.lower()} "
        f"and {validated_brief.exit_idea.lower()}."
    )
    generated_code = (
        f"// generated cBot draft for {strategy_id}\n"
        f"// goal: {validated_brief.goal}\n"
        f"// risk_per_trade: {validated_config.risk_per_trade}"
    )

    return StrategyDraft(
        strategy_id=strategy_id,
        plain_english_summary=summary,
        generated_code=generated_code,
        review_status="pending",
    )
