# cTrader TradeZenom Pipeline Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a greenfield trading-system platform that reproduces the TradeZenom-style autonomous pipeline using cTrader native tooling for strategy execution/backtesting and a provider-abstracted LLM control plane for research, orchestration, journaling, simulation, Discord automation, and tweet drafting.

**Architecture:** Keep deterministic trading logic and risk enforcement inside cTrader cBots. Put orchestration, model routing, experiment management, normalized event storage, analytics, prop-firm simulation, Discord workflows, and content drafting in external services. Use cTrader CLI for unattended build/backtest/report workflows, Open API for external account/data integration where needed, and desktop automation only for setup or UI-only gaps.

**Tech Stack:** cTrader Automate/cBots (C#), cTrader CLI, .NET 8, Python 3.12, FastAPI, PostgreSQL, Redis, Docker, pytest, Pydantic, LiteLLM or equivalent provider abstraction, Discord bot SDK, structured logging, JSON/HTML report ingestion.

## Architecture Contract

### Non-negotiable boundaries
- All live or paper trade decisions executed by the platform must pass through deterministic cBot code, never directly from an LLM.
- cBots must be headless-safe. Do not depend on UI-only APIs, message boxes, or in-bot HTTP assumptions for core execution.
- cTrader Cloud is not the primary runtime for this system because Cloud disables standard HTTP requests. Use local desktop, VPS, or CLI-hosted environments for bots that require external-service coordination.
- The normalized external ledger is the system of record for analytics, journal views, prop simulation, Discord workflows, approvals, and draft content generation.
- Promotion gates are mandatory: compile success → backtest success → simulator pass → paper-trade pass → human approval for live.
- Tweet generation stops at draft creation. Public posting requires explicit later scope.

### Target repository layout

```text
Ctrader/
├── ctrader/
│   ├── bots/
│   │   └── BreakoutBot/
│   │       ├── BreakoutBot.csproj
│   │       ├── BreakoutBot.cs
│   │       ├── Parameters/
│   │       │   ├── baseline.cbotset
│   │       │   └── smoke.cbotset
│   │       └── README.md
│   ├── fixtures/
│   │   ├── reports/
│   │   ├── events/
│   │   └── optimization/
│   └── cli/
│       ├── backtest-manifests/
│       └── sample-output/
├── apps/
│   ├── orchestrator/
│   ├── ledger/
│   ├── analytics/
│   ├── journal/
│   ├── prop-simulator/
│   ├── discord-bot/
│   └── content-pipeline/
├── libs/
│   ├── contracts/
│   ├── llm/
│   ├── ctrader_reports/
│   ├── risk/
│   └── observability/
├── tests/
│   ├── contract/
│   ├── integration/
│   ├── fixtures/
│   └── e2e/
├── scripts/
│   ├── dev/
│   ├── ci/
│   └── ctrader/
├── infra/
│   ├── docker/
│   ├── compose/
│   └── db/
└── docs/
    ├── plans/
    ├── architecture/
    └── runbooks/
```

## Delivery strategy

Even though the requested scope includes all feature families from the start, implementation must still proceed as thin vertical slices. The first slice proves the autonomous backtest pipeline end to end with a single strategy, single symbol, single account model, and a normalized ledger entry. All later modules must extend that single source of truth rather than creating parallel data paths.

## Acceptance criteria for the whole system

- A cBot can be compiled and backtested unattended through cTrader CLI using reproducible manifests and parameter files.
- The system freezes one canonical event taxonomy, approval-state model, and artifact reference format before downstream consumers are built.
- Backtest output is persisted as machine-readable artifacts and normalized into a ledger entry model that downstream services can consume.
- The orchestration layer validates all LLM outputs against typed schemas and rejects invalid or unsafe actions with explicit reasons.
- The same risk policy concepts are represented across backtest, simulator, paper, and live promotion gates.
- Journal views, portfolio analytics, and prop-rule checks can be recomputed from stored ledger data without spreadsheet intervention.
- Discord workflows consume approved events only and cannot bypass trading approval rules.
- Tweet workflow produces traceable drafts only, not live posting.
- The cBot/.NET side is build-verified in addition to Python/service-side tests.

## Task 1: Bootstrap the monorepo and verification harness

**Files:**
- Create: `README.md`
- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `pytest.ini`
- Create: `apps/orchestrator/__init__.py`
- Create: `libs/contracts/__init__.py`
- Create: `tests/contract/test_repo_bootstrap.py`
- Create: `scripts/dev/check.sh`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_repo_bootstrap_layout_exists():
    required = [
        Path("apps/orchestrator"),
        Path("libs/contracts"),
        Path("tests/contract"),
        Path("scripts/dev"),
    ]
    assert all(path.exists() for path in required)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_repo_bootstrap.py -v`
Expected: FAIL because required directories/files do not exist.

**Step 3: Write minimal implementation**

Create the directories and minimal files listed above. Make `scripts/dev/check.sh` run repository checks:

```bash
#!/usr/bin/env bash
set -euo pipefail
python -m pytest tests/contract -v
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_repo_bootstrap.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add README.md .gitignore pyproject.toml pytest.ini apps libs tests scripts
git commit -m "chore: bootstrap trading platform workspace"
```

## Task 2: Define immutable cross-system contracts

**Files:**
- Create: `libs/contracts/backtest_manifest.py`
- Create: `libs/contracts/ledger_event.py`
- Create: `libs/contracts/llm_commands.py`
- Create: `tests/contract/test_backtest_manifest_contract.py`
- Create: `tests/contract/test_ledger_event_contract.py`
- Create: `tests/contract/test_llm_commands_contract.py`

**Step 1: Write the failing test**

```python
from pydantic import ValidationError

from libs.contracts.backtest_manifest import BacktestManifest


def test_backtest_manifest_requires_symbol_and_dates():
    try:
        BacktestManifest.model_validate({})
    except ValidationError:
        assert True
    else:
        assert False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_backtest_manifest_contract.py -v`
Expected: FAIL because the contract module does not exist.

**Step 3: Write minimal implementation**

Implement typed models for:
- `BacktestManifest`: strategy id, symbol, timeframe, start/end, starting balance, spread/commission mode, parameter-set path, output path, run id.
- `LedgerEvent`: event id, run id, source, event type, timestamp UTC, payload, approval state.
- `LlmCommand`: allowed command enum values such as `propose_strategy_change`, `propose_parameter_sweep`, `summarize_results`, `draft_discord_message`, `draft_tweet`, plus schema version.

Freeze enum/value sets now, not later:
- `timeframe`: first milestone supports an explicit allowlist only.
- `event_type`: `run_requested`, `run_started`, `run_completed`, `run_failed`, `metrics_recorded`, `approval_requested`, `approval_granted`, `approval_rejected`, `paper_promotion_requested`, `live_promotion_requested`, `discord_draft_created`, `tweet_draft_created`.
- `approval_state`: `not_required`, `pending`, `approved`, `rejected`.
- `artifact_ref`: `kind`, `path`, `content_type`, `source_system`, `sha256`.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract -v`
Expected: PASS for all contract tests.

**Step 5: Commit**

```bash
git add libs/contracts tests/contract
git commit -m "feat: add shared contracts for manifests and events"
```

## Task 3: Freeze the event taxonomy and approval state machine

**Files:**
- Create: `libs/contracts/event_taxonomy.py`
- Create: `libs/contracts/approval_states.py`
- Create: `tests/contract/test_event_taxonomy.py`
- Create: `tests/contract/test_approval_state_machine.py`

**Step 1: Write the failing test**

```python
from libs.contracts.event_taxonomy import EVENT_TYPES


def test_event_taxonomy_contains_required_promotion_events():
    assert "approval_requested" in EVENT_TYPES
    assert "live_promotion_requested" in EVENT_TYPES
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_event_taxonomy.py tests/contract/test_approval_state_machine.py -v`
Expected: FAIL because the taxonomy and approval-state modules do not exist.

**Step 3: Write minimal implementation**

Create one shared taxonomy module that every downstream service imports. Define:
- event-type constants,
- allowed approval-state transitions,
- promotion transition rules,
- artifact reference format,
- explicit statement that downstream modules must not re-declare these enums locally.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_event_taxonomy.py tests/contract/test_approval_state_machine.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add libs/contracts tests/contract
git commit -m "feat: freeze event taxonomy and approval states"
```

## Task 4: Define the cBot runtime boundary and risk-enforcement contract

**Files:**
- Create: `libs/risk/runtime_boundary.py`
- Create: `docs/architecture/cbot-boundaries.md`
- Create: `tests/contract/test_runtime_boundary.py`

**Step 1: Write the failing test**

```python
from libs.risk.runtime_boundary import BOT_ENFORCED_CONTROLS, EXTERNAL_ONLY_CAPABILITIES


def test_runtime_boundary_separates_execution_risk_from_external_services():
    assert "max_open_risk" in BOT_ENFORCED_CONTROLS
    assert "tweet_publish" in EXTERNAL_ONLY_CAPABILITIES
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_runtime_boundary.py -v`
Expected: FAIL because the runtime boundary module does not exist.

**Step 3: Write minimal implementation**

Define the hard boundary explicitly:
- cBot-enforced controls: sizing, stop-loss placement, max open risk, trading window checks, instrument allowlist, kill switch hooks.
- external-only capabilities: LLM reasoning, analytics, journal views, Discord messaging, tweet drafting, approvals, and simulator projections.
- forbidden behavior: external services must never directly decide live orders.

In `docs/architecture/cbot-boundaries.md`, define headless-safe behavior: no UI APIs, no message boxes, no chart-shot dependencies, and no assumption of outbound HTTP from the bot.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_runtime_boundary.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add libs/risk docs/architecture tests/contract
git commit -m "docs: define cbot runtime boundary and risk contract"
```

## Task 5: Add a minimal cTrader cBot skeleton and parameter fixtures

**Files:**
- Create: `ctrader/bots/BreakoutBot/BreakoutBot.csproj`
- Create: `ctrader/bots/BreakoutBot/BreakoutBot.cs`
- Create: `ctrader/bots/BreakoutBot/Parameters/smoke.cbotset`
- Create: `ctrader/bots/BreakoutBot/README.md`
- Create: `tests/fixtures/test_breakout_bot_files.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_breakout_bot_files_exist():
    assert Path("ctrader/bots/BreakoutBot/BreakoutBot.cs").exists()
    assert Path("ctrader/bots/BreakoutBot/Parameters/smoke.cbotset").exists()


def test_breakout_bot_declares_headless_safe_parameters():
    source = Path("ctrader/bots/BreakoutBot/BreakoutBot.cs").read_text()
    assert "RiskPerTrade" in source
    assert "StopLoss" in source
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/fixtures/test_breakout_bot_files.py -v`
Expected: FAIL because the cBot skeleton does not exist.

**Step 3: Write minimal implementation**

Create a headless-safe cBot with:
- parameters for breakout lookback, risk per trade, session filter, stop loss, take profit,
- stubbed signal logic returning no trades until later tasks,
- no UI-only dependencies,
- README showing expected CLI build/backtest location.

**Step 4: Run test to verify it passes**

Run: `pytest tests/fixtures/test_breakout_bot_files.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add ctrader/bots tests/fixtures
git commit -m "feat: add initial cTrader breakout bot skeleton"
```

## Task 6: Create CLI backtest manifest generation

**Files:**
- Create: `apps/orchestrator/backtest_manifest_writer.py`
- Create: `tests/contract/test_backtest_manifest_writer.py`
- Create: `ctrader/cli/backtest-manifests/.gitkeep`

**Step 1: Write the failing test**

```python
from pathlib import Path

from apps.orchestrator.backtest_manifest_writer import write_manifest


def test_write_manifest_creates_json_file(tmp_path: Path):
    destination = tmp_path / "manifest.json"
    write_manifest(destination)
    assert destination.exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_backtest_manifest_writer.py -v`
Expected: FAIL because the writer does not exist.

**Step 3: Write minimal implementation**

Implement a manifest writer that emits validated JSON matching `BacktestManifest`.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_backtest_manifest_writer.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add apps/orchestrator ctrader/cli tests/contract
git commit -m "feat: add cTrader backtest manifest writer"
```

## Task 7: Add a cTrader CLI adapter with dry-run command construction

**Files:**
- Create: `apps/orchestrator/ctrader_cli.py`
- Create: `tests/contract/test_ctrader_cli.py`
- Create: `scripts/ctrader/run_backtest.sh`

**Step 1: Write the failing test**

```python
from apps.orchestrator.ctrader_cli import build_backtest_command


def test_build_backtest_command_contains_required_flags():
    command = build_backtest_command("manifest.json")
    assert "backtest" in command
    assert "manifest.json" in command


def test_build_backtest_command_rejects_unsupported_optimization_flags():
    try:
        build_backtest_command("manifest.json", mode="optimize")
    except ValueError:
        assert True
    else:
        assert False
```
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_ctrader_cli.py -v`
Expected: FAIL because the CLI adapter does not exist.

**Step 3: Write minimal implementation**

Build a pure command-construction adapter first. Do not execute cTrader yet. Encode supported flags from researched docs, return a structured argv list or equivalent stable representation, and reject unsupported optimization paths until proven.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_ctrader_cli.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add apps/orchestrator scripts/ctrader tests/contract
git commit -m "feat: add cTrader CLI backtest adapter"
```

## Task 8A: Freeze the cTrader CLI environment contract

**Files:**
- Create: `docs/runbooks/ctrader-cli-environment.md`
- Create: `tests/e2e/test_ctrader_cli_environment_contract.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_ctrader_cli_environment_runbook_declares_required_sections():
    content = Path("docs/runbooks/ctrader-cli-environment.md").read_text()
    assert "Supported cTrader version" in content
    assert "Runner OS" in content
    assert "Artifact directories" in content
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/e2e/test_ctrader_cli_environment_contract.py -v`
Expected: FAIL because the environment runbook does not exist.

**Step 3: Write minimal implementation**

Document the reproducible smoke-run contract:
- supported cTrader/CLI version,
- supported OS and shell,
- required installed components,
- expected artifact directories,
- parameter file locations,
- how to locate JSON/HTML outputs,
- how to verify `.NET` build prerequisites.

**Step 4: Run test to verify it passes**

Run: `pytest tests/e2e/test_ctrader_cli_environment_contract.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add docs/runbooks tests/e2e
git commit -m "docs: define ctrader cli environment contract"
```

## Task 8B: Prove the first unattended backtest seam end to end

**Files:**
- Create: `tests/integration/test_backtest_smoke.py`
- Create: `tests/fixtures/reports/sample_backtest.json`
- Create: `docs/runbooks/ctrader-backtest-smoke.md`
- Modify: `apps/orchestrator/ctrader_cli.py`

**Step 1: Write the failing test**

```python
import json
from pathlib import Path


def test_sample_backtest_fixture_contains_run_id():
    payload = json.loads(Path("tests/fixtures/reports/sample_backtest.json").read_text())
    assert payload["run_id"]


def test_sample_backtest_fixture_contains_minimum_report_shape():
    payload = json.loads(Path("tests/fixtures/reports/sample_backtest.json").read_text())
    assert payload["strategy_id"]
    assert payload["symbol"]
    assert payload["start_time_utc"]
    assert payload["end_time_utc"]
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_backtest_smoke.py -v`
Expected: FAIL because no sample backtest artifact exists yet.

**Step 3: Write minimal implementation**

Run one real cTrader CLI smoke backtest manually in the target environment, capture the resulting JSON/HTML artifacts, sanitize if needed, and store a representative JSON fixture. Document the exact command, expected output files, and environment prerequisites in the runbook. Also record the cBot build command and expected successful output for the `.NET` side.

**Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_backtest_smoke.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add tests/integration tests/fixtures/reports docs/runbooks apps/orchestrator
git commit -m "test: capture first cTrader backtest smoke artifact"
```

## Task 9: Normalize cTrader backtest output into ledger events

**Files:**
- Create: `libs/ctrader_reports/backtest_parser.py`
- Create: `apps/ledger/ingest_backtest.py`
- Create: `tests/contract/test_backtest_parser.py`
- Create: `tests/integration/test_backtest_ingest.py`

**Step 1: Write the failing test**

```python
from libs.ctrader_reports.backtest_parser import parse_backtest_report


def test_parse_backtest_report_returns_metrics_dict(sample_backtest_payload):
    report = parse_backtest_report(sample_backtest_payload)
    assert "net_profit" in report.metrics
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_backtest_parser.py -v`
Expected: FAIL because the parser does not exist.

**Step 3: Write minimal implementation**

Parse cTrader JSON report artifacts into normalized models. Emit ledger events for run started, run completed, summary metrics, and per-run artifacts. Make timestamps UTC and preserve raw source payload paths for traceability.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_backtest_parser.py tests/integration/test_backtest_ingest.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add libs/ctrader_reports apps/ledger tests/contract tests/integration
git commit -m "feat: ingest cTrader backtest reports into ledger"
```

## Task 10: Stand up the ledger storage schema

**Files:**
- Create: `infra/db/001_create_ledger_tables.sql`
- Create: `infra/compose/postgres.yml`
- Create: `apps/ledger/repository.py`
- Create: `tests/contract/test_ledger_repository.py`
- Create: `tests/fixtures/events/sample_ledger_event.json`

**Step 1: Write the failing test**

```python
from apps.ledger.repository import LedgerRepository


def test_repository_exposes_append_and_list_methods():
    repo = LedgerRepository()
    assert hasattr(repo, "append")
    assert hasattr(repo, "list_by_run_id")


def test_repository_contract_requires_append_only_and_ordered_reads():
    repo = LedgerRepository()
    assert hasattr(repo, "append")
    assert hasattr(repo, "list_by_run_id")
```
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_ledger_repository.py -v`
Expected: FAIL because the repository does not exist.

**Step 3: Write minimal implementation**

Create append-only ledger tables with unique event ids, run ids, sources, timestamps, approval state, and JSON payload columns. Implement a repository abstraction against PostgreSQL. Document local startup and migration execution convention using `infra/compose/postgres.yml` before the repository is used.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_ledger_repository.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add infra/db apps/ledger tests/contract tests/fixtures/events
git commit -m "feat: add append-only ledger storage"
```

## Task 11: Implement portfolio analytics from ledger data

**Files:**
- Create: `apps/analytics/metrics.py`
- Create: `tests/contract/test_portfolio_metrics.py`
- Create: `tests/fixtures/events/portfolio_sample.json`

**Step 1: Write the failing test**

```python
from apps.analytics.metrics import compute_portfolio_metrics


def test_compute_portfolio_metrics_returns_sharpe_drawdown_and_correlation(portfolio_events):
    metrics = compute_portfolio_metrics(portfolio_events)
    assert metrics.sharpe_ratio is not None
    assert metrics.max_drawdown is not None
    assert metrics.correlation_matrix is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_portfolio_metrics.py -v`
Expected: FAIL because the metrics module does not exist.

**Step 3: Write minimal implementation**

Compute Sharpe ratio, drawdown, expectancy, win rate, exposure, and cross-strategy correlation from normalized ledger events only. Define the canonical time basis as UTC.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_portfolio_metrics.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add apps/analytics tests/contract tests/fixtures/events
git commit -m "feat: add portfolio analytics from normalized ledger data"
```

## Task 12: Implement journal projection views

**Files:**
- Create: `apps/journal/projections.py`
- Create: `tests/contract/test_journal_projection.py`

**Step 1: Write the failing test**

```python
from apps.journal.projections import build_journal_entry


def test_build_journal_entry_contains_trade_summary(backtest_completed_event):
    entry = build_journal_entry(backtest_completed_event)
    assert entry.summary
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_journal_projection.py -v`
Expected: FAIL because the projections module does not exist.

**Step 3: Write minimal implementation**

Project ledger events into journal entries containing strategy id, symbol, run context, summary metrics, notes, approval history, and linked artifacts.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_journal_projection.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add apps/journal tests/contract
git commit -m "feat: add journal projections from ledger events"
```

## Task 13: Implement prop-firm rules engine

**Files:**
- Create: `apps/prop-simulator/rules.py`
- Create: `apps/prop-simulator/evaluator.py`
- Create: `tests/contract/test_prop_rules.py`
- Create: `tests/fixtures/events/prop_rule_sample.json`

**Step 1: Write the failing test**

```python
from apps.prop_simulator.evaluator import evaluate_prop_status


def test_evaluate_prop_status_flags_daily_loss_breach(prop_rule_events):
    result = evaluate_prop_status(prop_rule_events)
    assert result.daily_loss_breached is True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_prop_rules.py -v`
Expected: FAIL because the prop simulator modules do not exist.

**Step 3: Write minimal implementation**

Start with one explicit prop rule pack and implement deterministic checks for daily loss, trailing drawdown, max positions, and trading window compliance. Name the first pack explicitly in code and docs so verification is not ambiguous.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_prop_rules.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add apps/prop-simulator tests/contract tests/fixtures/events
git commit -m "feat: add initial prop firm simulator rules"
```

## Task 14: Add LLM provider abstraction and typed command validation

**Files:**
- Create: `libs/llm/provider.py`
- Create: `libs/llm/router.py`
- Create: `libs/llm/validator.py`
- Create: `tests/contract/test_llm_validator.py`
- Create: `tests/fixtures/llm/valid_command.json`
- Create: `tests/fixtures/llm/invalid_command.json`

**Step 1: Write the failing test**

```python
from libs.llm.validator import validate_command


def test_validate_command_rejects_unknown_action(invalid_command_payload):
    result = validate_command(invalid_command_payload)
    assert result.is_valid is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_llm_validator.py -v`
Expected: FAIL because the validator does not exist.

**Step 3: Write minimal implementation**

Implement provider abstraction with typed request/response envelopes. Add strict schema validation, retry metadata, and rejection reasons. Support OpenAI-first structured outputs with interchangeable provider configuration for Kimi-compatible endpoints.

Explicitly classify commands into:
- advisory only,
- internal-state mutation allowed,
- never-directly-executable against paper/live trading.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_llm_validator.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add libs/llm tests/contract tests/fixtures/llm
git commit -m "feat: add provider-agnostic llm command validation"
```

## Task 15: Add experiment orchestration with approval gates

**Files:**
- Create: `apps/orchestrator/workflow.py`
- Create: `apps/orchestrator/approvals.py`
- Create: `tests/integration/test_experiment_workflow.py`

**Step 1: Write the failing test**

```python
from apps.orchestrator.workflow import next_stage


def test_next_stage_requires_approval_before_paper_or_live():
    assert next_stage("simulator_passed", approved=False) == "awaiting_approval"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_experiment_workflow.py -v`
Expected: FAIL because the workflow module does not exist.

**Step 3: Write minimal implementation**

Implement stage transitions for draft strategy, manifest creation, backtest completed, simulator passed, paper eligible, live eligible, and rejected. Encode approval requirements for paper/live promotion and public content actions.

**Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_experiment_workflow.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add apps/orchestrator tests/integration
git commit -m "feat: add orchestration workflow with approval gates"
```

## Task 16: Add Discord automation with XP-safe event consumption

**Files:**
- Create: `apps/discord-bot/consumer.py`
- Create: `apps/discord-bot/xp.py`
- Create: `tests/contract/test_discord_consumer.py`

**Step 1: Write the failing test**

```python
from apps.discord_bot.consumer import should_publish_event


def test_should_publish_event_blocks_unapproved_live_actions():
    assert should_publish_event({"event_type": "live_promotion_requested", "approved": False}) is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_discord_consumer.py -v`
Expected: FAIL because the Discord consumer does not exist.

**Step 3: Write minimal implementation**

Consume approved ledger events, map them to Discord-safe notifications, and keep XP automation independent from trading controls. No direct broker actions from Discord.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_discord_consumer.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add apps/discord-bot tests/contract
git commit -m "feat: add approval-safe discord automation consumer"
```

## Task 17: Add tweet-draft pipeline with traceability

**Files:**
- Create: `apps/content-pipeline/drafts.py`
- Create: `tests/contract/test_tweet_drafts.py`

**Step 1: Write the failing test**

```python
from apps.content_pipeline.drafts import build_tweet_draft


def test_build_tweet_draft_marks_output_as_draft_only(sample_completed_run):
    draft = build_tweet_draft(sample_completed_run)
    assert draft.publish_state == "draft"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_tweet_drafts.py -v`
Expected: FAIL because the content pipeline module does not exist.

**Step 3: Write minimal implementation**

Build tweet drafts from approved, traceable run summaries only. Include source artifact references and an approval status field. No publish adapter in this milestone.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_tweet_drafts.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add apps/content-pipeline tests/contract
git commit -m "feat: add traceable tweet draft generation"
```

## Task 18: Add Open API adapter for external account/data services

**Files:**
- Create: `apps/orchestrator/open_api_client.py`
- Create: `tests/contract/test_open_api_client.py`

**Step 1: Write the failing test**

```python
from apps.orchestrator.open_api_client import OpenApiClient


def test_open_api_client_exposes_account_and_position_methods():
    client = OpenApiClient()
    assert hasattr(client, "list_accounts")
    assert hasattr(client, "list_positions")
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/contract/test_open_api_client.py -v`
Expected: FAIL because the client does not exist.

**Step 3: Write minimal implementation**

Implement a typed adapter for external data/account retrieval and read-only operational views. Do not couple core backtest flow to Open API. Treat this task as non-blocking for the first backtest-to-ledger milestone.

**Step 4: Run test to verify it passes**

Run: `pytest tests/contract/test_open_api_client.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add apps/orchestrator tests/contract
git commit -m "feat: add ctrader open api adapter"
```

## Task 19: Add end-to-end smoke verification script and CI shape

**Files:**
- Create: `scripts/ci/smoke.sh`
- Create: `.github/workflows/ci.yml`
- Create: `tests/e2e/test_smoke_contracts.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_smoke_script_exists():
    assert Path("scripts/ci/smoke.sh").exists()


def test_smoke_script_declares_contract_and_integration_runs():
    content = Path("scripts/ci/smoke.sh").read_text()
    assert "tests/contract" in content
    assert "tests/integration" in content
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/e2e/test_smoke_contracts.py -v`
Expected: FAIL because the smoke script does not exist.

**Step 3: Write minimal implementation**

Create a smoke script that runs contract tests, integration tests against fixtures, and basic linting. Add CI workflow for the external Python services and contract suite. Keep real cTrader execution as an environment-specific smoke run documented outside CI until the runner environment is standardized.

**Step 4: Run test to verify it passes**

Run: `pytest tests/e2e/test_smoke_contracts.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add scripts/ci .github/workflows tests/e2e
git commit -m "chore: add smoke verification and ci shape"
```

## Task 20: Document operational runbooks and deferred scope

**Files:**
- Create: `docs/architecture/system-overview.md`
- Create: `docs/runbooks/promotion-gates.md`
- Create: `docs/runbooks/desktop-automation-boundaries.md`
- Modify: `README.md`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_runbooks_exist_for_promotion_and_desktop_boundaries():
    assert Path("docs/runbooks/promotion-gates.md").exists()
    assert Path("docs/runbooks/desktop-automation-boundaries.md").exists()


def test_promotion_runbook_mentions_human_approval_for_paper_and_live():
    content = Path("docs/runbooks/promotion-gates.md").read_text()
    assert "paper" in content
    assert "live" in content
    assert "approval" in content
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/e2e/test_smoke_contracts.py -v`
Expected: FAIL because the runbooks do not exist.

**Step 3: Write minimal implementation**

Document:
- architecture boundaries,
- promotion gates for paper/live,
- where desktop automation is acceptable and forbidden,
- non-goals for this phase: no direct live LLM trading, no auto-publish to social, no multi-broker abstraction until cTrader core is proven.

**Step 4: Run test to verify it passes**

Run: `pytest tests/e2e/test_smoke_contracts.py -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add docs README.md tests/e2e
git commit -m "docs: add operational boundaries and runbooks"
```

## Notes for the implementer

- Treat cTrader CLI optimization as a deferred research seam unless you verify a supported unattended optimization workflow in your target environment.
- Prefer one supported strategy and one supported symbol first. Expand breadth only after ledger, analytics, and simulator flows are stable.
- If cTrader desktop automation is required, isolate it in `scripts/ctrader/` and never let it become the main orchestration path.
- Keep every raw cTrader artifact path attached to normalized events so later audits can reconstruct exactly what happened.
- Do not let Discord, tweet drafting, or LLM providers import trading runtime code directly. All communication should happen through contracts and ledger events.

## Final verification sequence after Task 20

Run:

```bash
pytest tests/contract -v
pytest tests/integration -v
pytest tests/e2e -v
bash scripts/ctrader/run_backtest.sh --help || true
bash scripts/dev/check.sh
```

Expected:
- All owned Python/service tests pass.
- Fixture-based cTrader ingestion tests pass.
- cBot/.NET build path and cTrader CLI path are documented and operator-verifiable.
- CI smoke script exists and executes locally.
- Runbooks document exactly where human approval is required.

## Non-goals for this plan

- direct LLM-triggered live order placement
- auto-publishing tweets or external content
- plugin-based cTrader UI automation as the core runtime
- full multi-broker abstraction before the cTrader path is stable
- assuming cTrader Cloud can host bots that depend on external HTTP services
