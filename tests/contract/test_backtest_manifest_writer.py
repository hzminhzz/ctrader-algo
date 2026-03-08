from pathlib import Path

from apps.orchestrator.backtest_manifest_writer import write_manifest


def test_write_manifest_creates_json_file(tmp_path: Path) -> None:
    destination = tmp_path / "manifest.json"
    write_manifest(destination)
    assert destination.exists()
