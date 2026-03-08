CREATE TABLE ledger_events (
    event_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    source TEXT NOT NULL,
    event_type TEXT NOT NULL,
    timestamp_utc TIMESTAMPTZ NOT NULL,
    approval_state TEXT NOT NULL,
    payload JSONB NOT NULL,
    artifact_ref JSONB
);
