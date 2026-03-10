from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from apps.operator_ui.drafting import generate_strategy_draft
from apps.operator_ui.review import build_review_checklist, can_run_backtest
from apps.operator_ui.workflow import prepare_backtest_request, summarize_run_evaluation

STAGES = ("Create", "Review", "Backtest", "Evaluate", "Promote")


def reset_operator_state_for_new_draft(session_state: dict[str, object]) -> None:
    session_state["review_complete"] = False
    session_state["backtest_request"] = None
    session_state["evaluation_summary"] = None


def ensure_state() -> None:
    defaults = {
        "draft": None,
        "safe_config": None,
        "checklist": None,
        "review_complete": False,
        "backtest_request": None,
        "evaluation_summary": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def render_create_stage() -> None:
    st.header("Create")
    with st.form("strategy_create_form"):
        title = st.text_input("Strategy title", value="London breakout")
        goal = st.text_area("Goal", value="Trade London breakout moves")
        entry_idea = st.text_area("Entry idea", value="Buy breakout above range high")
        exit_idea = st.text_area("Exit idea", value="Exit at stop loss or take profit")
        risk_notes = st.text_area("Risk notes", value="Use 1 percent risk")
        symbol = st.text_input("Symbol", value="EURUSD")
        timeframe = st.selectbox(
            "Timeframe", ["M1", "M5", "M15", "M30", "H1", "H4", "D1"], index=4
        )
        risk_per_trade = st.number_input(
            "Risk per trade", min_value=0.001, max_value=1.0, value=0.01, step=0.001
        )
        session_filter = st.text_input("Session filter", value="London")
        promotion_target = st.selectbox("Promotion target", ["paper", "live"], index=0)
        submitted = st.form_submit_button("Generate strategy draft")

    if submitted:
        brief = {
            "title": title,
            "goal": goal,
            "entry_idea": entry_idea,
            "exit_idea": exit_idea,
            "risk_notes": risk_notes,
        }
        safe_config = {
            "symbol": symbol,
            "timeframe": timeframe,
            "risk_per_trade": risk_per_trade,
            "session_filter": session_filter,
            "promotion_target": promotion_target,
        }
        st.session_state.safe_config = safe_config
        reset_operator_state_for_new_draft(st.session_state)
        st.session_state.draft = generate_strategy_draft(
            brief=brief, safe_config=safe_config
        )
        st.session_state.checklist = build_review_checklist(
            strategy_summary=st.session_state.draft.plain_english_summary,
            safe_config=safe_config,
        )
    if st.session_state.draft is not None:
        st.subheader("Draft summary")
        st.write(st.session_state.draft.plain_english_summary)
        with st.expander("Advanced: generated code"):
            st.code(st.session_state.draft.generated_code, language="csharp")


def render_review_stage() -> None:
    st.header("Review")
    checklist = st.session_state.checklist
    if checklist is None:
        st.info("Generate a draft in Create before review starts.")
        return

    completed_flags: list[bool] = []
    for item in checklist.items:
        completed_flags.append(
            st.checkbox(item.label, value=item.completed, key=item.label)
        )

    review_complete = all(completed_flags)
    st.session_state.review_complete = review_complete
    if review_complete:
        st.success("Review complete. Backtest can now be prepared.")
    else:
        st.warning("Complete every checklist item before backtest is enabled.")


def render_backtest_stage() -> None:
    st.header("Backtest")
    draft = st.session_state.draft
    safe_config = st.session_state.safe_config
    if draft is None or safe_config is None:
        st.info("Generate and review a strategy before preparing a backtest.")
        return

    checklist = st.session_state.checklist
    if checklist is None:
        st.info("Review checklist not available yet.")
        return

    effective_checklist = checklist.model_copy(
        update={"is_complete": st.session_state.review_complete}
    )
    if not can_run_backtest(effective_checklist):
        st.warning("Backtest is blocked until the review checklist is complete.")
        return

    if st.button("Prepare backtest request"):
        st.session_state.backtest_request = prepare_backtest_request(
            manifest_path=Path(
                "ctrader/cli/backtest-manifests/operator-generated.json"
            ),
            strategy_id=draft.strategy_id,
            safe_config=safe_config,
        )

    if st.session_state.backtest_request is not None:
        request = st.session_state.backtest_request
        st.write(request.operator_message)
        st.code(request.command)
        st.caption(f"Manifest path: {request.manifest_path}")


def render_evaluate_stage() -> None:
    st.header("Evaluate")
    if st.button("Load evaluation summary"):
        st.session_state.evaluation_summary = summarize_run_evaluation(
            report_payload_path=Path("tests/fixtures/reports/sample_backtest.json"),
            portfolio_events_path=Path("tests/fixtures/events/portfolio_sample.json"),
            prop_rule_events_path=Path("tests/fixtures/events/prop_rule_sample.json"),
            completed_event_path=Path("tests/fixtures/events/sample_ledger_event.json"),
        )

    if st.session_state.evaluation_summary is not None:
        summary = st.session_state.evaluation_summary
        st.write(f"Run ID: {summary['run_id']}")
        st.write(f"Journal summary: {summary['journal_summary']}")
        st.write(f"Promotion status: {summary['promotion_status']}")
        st.write(f"Sharpe ratio: {summary['sharpe_ratio']}")
        st.write(f"Max drawdown: {summary['max_drawdown']}")


def render_promote_stage() -> None:
    st.header("Promote")
    summary = st.session_state.evaluation_summary
    if summary is None:
        st.info("Load the evaluation summary before reviewing promotion status.")
        return
    st.write(f"Current promotion status: {summary['promotion_status']}")
    st.write("Paper and live promotion remain approval-gated.")


def main() -> None:
    st.set_page_config(page_title="Operator Lifecycle Workflow", layout="wide")
    ensure_state()
    st.title("Operator Lifecycle Workflow")
    selected_stage = st.sidebar.radio("Stage", STAGES)

    if selected_stage == "Create":
        render_create_stage()
    elif selected_stage == "Review":
        render_review_stage()
    elif selected_stage == "Backtest":
        render_backtest_stage()
    elif selected_stage == "Evaluate":
        render_evaluate_stage()
    else:
        render_promote_stage()


if __name__ == "__main__":
    main()
