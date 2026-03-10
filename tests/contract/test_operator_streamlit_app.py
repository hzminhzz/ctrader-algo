from pathlib import Path
import subprocess
import sys

from apps.operator_ui.streamlit_app import reset_operator_state_for_new_draft


def test_streamlit_operator_app_exists() -> None:
    assert Path("apps/operator_ui/streamlit_app.py").exists()


def test_streamlit_operator_app_module_loads_from_script_path() -> None:
    result = subprocess.run(
        [sys.executable, "apps/operator_ui/streamlit_app.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_reset_operator_state_for_new_draft_clears_stale_outputs() -> None:
    session_state: dict[str, object] = {
        "review_complete": True,
        "backtest_request": {"command": "old-command"},
        "evaluation_summary": {"promotion_status": "awaiting_approval"},
    }

    reset_operator_state_for_new_draft(session_state)

    assert session_state["review_complete"] is False
    assert session_state["backtest_request"] is None
    assert session_state["evaluation_summary"] is None
