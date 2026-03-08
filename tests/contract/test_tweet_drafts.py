import json
from importlib import import_module
from pathlib import Path
from typing import Callable, Protocol, cast


class TweetDraftLike(Protocol):
    publish_state: str


content_module = import_module("apps.content_pipeline.drafts")
build_tweet_draft = cast(
    Callable[[dict[str, object]], TweetDraftLike],
    content_module.build_tweet_draft,
)


def load_payload(path: str) -> dict[str, object]:
    return cast(dict[str, object], json.loads(Path(path).read_text()))


def test_build_tweet_draft_marks_output_as_draft_only() -> None:
    sample_completed_run = load_payload("tests/fixtures/reports/sample_backtest.json")

    draft = build_tweet_draft(sample_completed_run)

    assert draft.publish_state == "draft"
