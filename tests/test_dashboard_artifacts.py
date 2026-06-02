import json
from pathlib import Path


def test_committed_dashboard_artifact_contract() -> None:
    artifact = Path("public/results/benchmark-summary.json")
    assert artifact.exists()
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    assert payload["benchmark"]["scenario_count"] == 18
    assert {"leaderboard", "scenario_results", "scenarios"}.issubset(payload)
