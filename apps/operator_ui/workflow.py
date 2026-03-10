from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from apps.analytics.metrics import compute_portfolio_metrics
from apps.journal.projections import build_journal_entry
from apps.ledger.ingest_backtest import ingest_backtest_report
from apps.orchestrator.backtest_manifest_writer import write_manifest
from apps.orchestrator.ctrader_cli import build_backtest_command
from apps.orchestrator.workflow import next_stage
from apps.prop_simulator.evaluator import evaluate_prop_status
from libs.contracts.operator_workflow import SafeStrategyConfig


@dataclass(frozen=True)
class BacktestRequest:
    manifest_path: Path
    command: str
    operator_message: str


def prepare_backtest_request(
    *, manifest_path: Path, strategy_id: str, safe_config: dict[str, object]
) -> BacktestRequest:
    validated_config = SafeStrategyConfig.model_validate(safe_config)
    payload = {
        "strategy_id": strategy_id,
        "symbol": validated_config.symbol,
        "timeframe": validated_config.timeframe,
        "start": "2025-01-01T00:00:00Z",
        "end": "2025-01-31T00:00:00Z",
        "starting_balance": 10000,
        "spread_mode": "fixed",
        "commission_mode": "per_lot",
        "parameter_set_path": "ctrader/bots/BreakoutBot/Parameters/smoke.cbotset",
        "output_path": "ctrader/cli/runtime/report.json",
        "run_id": f"{strategy_id}-run",
    }
    write_manifest(manifest_path, payload)
    command_parts = build_backtest_command(str(manifest_path))
    command = " ".join(command_parts)
    message = (
        f"Backtest prepared for {validated_config.symbol} {validated_config.timeframe}. "
        f"Use the generated command when the review gate is complete."
    )
    return BacktestRequest(
        manifest_path=manifest_path, command=command, operator_message=message
    )


def load_json(path: Path) -> object:
    return json.loads(path.read_text())


def summarize_run_evaluation(
    *,
    report_payload_path: Path,
    portfolio_events_path: Path,
    prop_rule_events_path: Path,
    completed_event_path: Path,
) -> dict[str, object]:
    report_payload = load_json(report_payload_path)
    portfolio_events = load_json(portfolio_events_path)
    prop_rule_events = load_json(prop_rule_events_path)
    completed_event = load_json(completed_event_path)

    ingested_events = ingest_backtest_report(report_payload)
    metrics = compute_portfolio_metrics(portfolio_events)
    journal_entry = build_journal_entry(completed_event)
    prop_status = evaluate_prop_status(prop_rule_events)

    simulator_passed = not any(
        (
            prop_status.daily_loss_breached,
            prop_status.trailing_drawdown_breached,
            prop_status.max_positions_breached,
            prop_status.trading_window_breached,
        )
    )
    promotion_status = (
        next_stage("simulator_passed", approved=False)
        if simulator_passed
        else "simulator_failed"
    )

    return {
        "run_id": report_payload["run_id"],
        "event_types": [event.event_type for event in ingested_events],
        "journal_summary": journal_entry.summary,
        "promotion_status": promotion_status,
        "sharpe_ratio": metrics.sharpe_ratio,
        "max_drawdown": metrics.max_drawdown,
        "daily_loss_breached": prop_status.daily_loss_breached,
        "trailing_drawdown_breached": prop_status.trailing_drawdown_breached,
        "max_positions_breached": prop_status.max_positions_breached,
        "trading_window_breached": prop_status.trading_window_breached,
    }
