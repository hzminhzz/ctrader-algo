from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TweetDraft:
    publish_state: str
    text: str
    source_artifact: str


def build_tweet_draft(sample_completed_run: dict[str, object]) -> TweetDraft:
    strategy_id = str(sample_completed_run.get("strategy_id", "unknown-strategy"))
    symbol = str(sample_completed_run.get("symbol", "unknown-symbol"))
    run_id = str(sample_completed_run.get("run_id", "unknown-run"))
    return TweetDraft(
        publish_state="draft",
        text=f"{strategy_id} finished a run on {symbol} ({run_id}).",
        source_artifact="tests/fixtures/reports/sample_backtest.json",
    )
