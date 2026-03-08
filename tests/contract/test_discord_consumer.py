from importlib import import_module
from typing import Callable, cast


discord_module = import_module("apps.discord_bot.consumer")
should_publish_event = cast(
    Callable[[dict[str, object]], bool], discord_module.should_publish_event
)


def test_should_publish_event_blocks_unapproved_live_actions() -> None:
    assert (
        should_publish_event(
            {"event_type": "live_promotion_requested", "approved": False}
        )
        is False
    )
