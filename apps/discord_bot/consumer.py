from __future__ import annotations


def should_publish_event(event: dict[str, object]) -> bool:
    if event.get("event_type") == "live_promotion_requested" and not event.get(
        "approved", False
    ):
        return False
    return True
