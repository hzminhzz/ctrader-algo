def requires_approval(stage: str) -> bool:
    return stage in {"simulator_passed", "paper_eligible", "live_eligible"}
