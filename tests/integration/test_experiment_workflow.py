from importlib import import_module
from typing import Callable, cast


workflow_module = import_module("apps.orchestrator.workflow")
next_stage = cast(Callable[..., str], workflow_module.next_stage)


def test_next_stage_requires_approval_before_paper_or_live() -> None:
    assert next_stage("simulator_passed", approved=False) == "awaiting_approval"
