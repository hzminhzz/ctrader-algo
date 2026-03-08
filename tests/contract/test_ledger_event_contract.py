from datetime import datetime
from zoneinfo import ZoneInfo

from collections.abc import Mapping
from types import MappingProxyType

import pytest
from pydantic import ValidationError

from libs.contracts.ledger_event import LedgerEvent


def test_ledger_event_requires_identity_and_payload() -> None:
    with pytest.raises(ValidationError):
        _ = LedgerEvent.model_validate({})


def test_ledger_event_accepts_valid_payload() -> None:
    event = LedgerEvent.model_validate(
        {
            "event_id": "evt-001",
            "run_id": "run-001",
            "source": "ctrader_cli",
            "event_type": "run_completed",
            "timestamp_utc": "2025-01-31T12:00:00Z",
            "payload": {"net_profit": 1250.5},
            "approval_state": "not_required",
        }
    )

    assert event.event_type == "run_completed"
    assert event.approval_state == "not_required"


def test_ledger_event_accepts_semantic_utc_timezone() -> None:
    event = LedgerEvent.model_validate(
        {
            "event_id": "evt-001",
            "run_id": "run-001",
            "source": "ctrader_cli",
            "event_type": "run_completed",
            "timestamp_utc": datetime(2025, 1, 31, 12, 0, 0, tzinfo=ZoneInfo("UTC")),
            "payload": {"net_profit": 1250.5},
            "approval_state": "not_required",
        }
    )

    assert event.timestamp_utc.utcoffset() is not None


def test_ledger_event_rejects_non_utc_timestamp() -> None:
    with pytest.raises(ValidationError):
        _ = LedgerEvent.model_validate(
            {
                "event_id": "evt-001",
                "run_id": "run-001",
                "source": "ctrader_cli",
                "event_type": "run_completed",
                "timestamp_utc": "2025-01-31T12:00:00+07:00",
                "payload": {"net_profit": 1250.5},
                "approval_state": "not_required",
            }
        )


def test_ledger_event_rejects_invalid_event_type() -> None:
    with pytest.raises(ValidationError):
        _ = LedgerEvent.model_validate(
            {
                "event_id": "evt-001",
                "run_id": "run-001",
                "source": "ctrader_cli",
                "event_type": "unknown_event",
                "timestamp_utc": "2025-01-31T12:00:00Z",
                "payload": {"net_profit": 1250.5},
                "approval_state": "not_required",
            }
        )


def test_ledger_event_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        _ = LedgerEvent.model_validate(
            {
                "event_id": "evt-001",
                "run_id": "run-001",
                "source": "ctrader_cli",
                "event_type": "run_completed",
                "timestamp_utc": "2025-01-31T12:00:00Z",
                "payload": {"net_profit": 1250.5},
                "approval_state": "not_required",
                "unexpected": True,
            }
        )


def test_ledger_event_rejects_empty_identifiers() -> None:
    with pytest.raises(ValidationError):
        _ = LedgerEvent.model_validate(
            {
                "event_id": "",
                "run_id": "   ",
                "source": "",
                "event_type": "run_completed",
                "timestamp_utc": "2025-01-31T12:00:00Z",
                "payload": {"net_profit": 1250.5},
                "approval_state": "not_required",
            }
        )


def test_ledger_event_rejects_non_json_payload_with_validation_error() -> None:
    with pytest.raises(ValidationError):
        _ = LedgerEvent.model_validate(
            {
                "event_id": "evt-001",
                "run_id": "run-001",
                "source": "ctrader_cli",
                "event_type": "run_completed",
                "timestamp_utc": "2025-01-31T12:00:00Z",
                "payload": {"bad": {1, 2, 3}},
                "approval_state": "not_required",
            }
        )


def test_ledger_event_validates_nested_artifact_ref() -> None:
    with pytest.raises(ValidationError):
        _ = LedgerEvent.model_validate(
            {
                "event_id": "evt-001",
                "run_id": "run-001",
                "source": "ctrader_cli",
                "event_type": "run_completed",
                "timestamp_utc": "2025-01-31T12:00:00Z",
                "payload": {"net_profit": 1250.5},
                "approval_state": "not_required",
                "artifact_ref": {"kind": "report"},
            }
        )


def test_ledger_event_rejects_empty_artifact_fields() -> None:
    with pytest.raises(ValidationError):
        _ = LedgerEvent.model_validate(
            {
                "event_id": "evt-001",
                "run_id": "run-001",
                "source": "ctrader_cli",
                "event_type": "run_completed",
                "timestamp_utc": "2025-01-31T12:00:00Z",
                "payload": {"net_profit": 1250.5},
                "approval_state": "not_required",
                "artifact_ref": {
                    "kind": "",
                    "path": "",
                    "content_type": "",
                    "source_system": "",
                    "sha256": "",
                },
            }
        )


def test_ledger_event_is_immutable() -> None:
    event = LedgerEvent.model_validate(
        {
            "event_id": "evt-001",
            "run_id": "run-001",
            "source": "ctrader_cli",
            "event_type": "run_completed",
            "timestamp_utc": "2025-01-31T12:00:00Z",
            "payload": {"net_profit": 1250.5},
            "approval_state": "not_required",
        }
    )

    with pytest.raises(ValidationError):
        event.source = "manual"


def test_ledger_event_payload_is_deeply_immutable() -> None:
    event = LedgerEvent.model_validate(
        {
            "event_id": "evt-001",
            "run_id": "run-001",
            "source": "ctrader_cli",
            "event_type": "run_completed",
            "timestamp_utc": "2025-01-31T12:00:00Z",
            "payload": {"details": {"count": 1}, "values": [1, 2, 3]},
            "approval_state": "not_required",
        }
    )

    details = event.payload["details"]
    values = event.payload["values"]

    assert isinstance(event.payload, MappingProxyType)
    assert isinstance(details, Mapping)
    assert isinstance(details, MappingProxyType)
    assert isinstance(values, tuple)
    assert values == (1, 2, 3)
