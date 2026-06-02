from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals"))

from agenteval import FlawedAgentRunner, ReferenceAgentRunner, evaluate_run, load_scenarios, summarize_results


RUNNERS = {
    "reference": ReferenceAgentRunner,
    "flawed": FlawedAgentRunner,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AgentEval benchmark and export dashboard artifacts.")
    parser.add_argument("--agents", nargs="+", default=["reference", "flawed"], choices=sorted(RUNNERS))
    parser.add_argument("--scenarios", default="scenarios/aerospace_synthetic_v0.jsonl")
    parser.add_argument("--output", default="public/results")
    args = parser.parse_args()

    scenarios = load_scenarios(args.scenarios)
    runners = [RUNNERS[name]() for name in args.agents]
    results = []
    for runner in runners:
        for scenario in scenarios:
            run = runner.run(scenario)
            results.append(evaluate_run(scenario, run))

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    leaderboard = summarize_results(results)
    scenario_rows = [_scenario_result_row(result) for result in results]
    benchmark_summary = {
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "benchmark": {
            "name": "Industrial Agent Reliability Benchmark",
            "version": "aerospace_synthetic_v0",
            "scenario_count": len(scenarios),
            "agent_count": len(runners),
            "categories": sorted({scenario.category for scenario in scenarios}),
            "metric_weights": {
                "task_completion": 0.28,
                "tool_call_accuracy": 0.24,
                "loop_termination": 0.18,
                "grounding": 0.18,
                "governance": 0.12,
            },
        },
        "leaderboard": leaderboard,
        "scenario_results": scenario_rows,
        "scenarios": [_public_scenario(scenario) for scenario in scenarios],
    }

    _write_json(output_dir / "benchmark-summary.json", benchmark_summary)
    _write_json(output_dir / "leaderboard.json", leaderboard)
    _write_json(output_dir / "scenario-results.json", scenario_rows)
    _write_csv(output_dir / "leaderboard.csv", leaderboard)
    print(f"Exported {len(results)} evaluations to {output_dir}")


def _scenario_result_row(result: Any) -> dict[str, Any]:
    metrics = {metric.name: asdict(metric) for metric in result.metrics}
    return {
        "agent": result.agent_name,
        "scenario_id": result.scenario_id,
        "composite_score": result.composite_score,
        "metrics": metrics,
        "tool_calls": [asdict(call) for call in result.run.tool_calls],
        "terminated": result.run.terminated,
        "steps": result.run.steps,
        "final_answer": result.run.final_answer,
    }


def _public_scenario(scenario: Any) -> dict[str, Any]:
    return {
        "id": scenario.id,
        "title": scenario.title,
        "category": scenario.category,
        "risk_level": scenario.risk_level,
        "prompt": scenario.prompt,
        "max_steps": scenario.max_steps,
        "allowed_tools": scenario.allowed_tools,
        "expected_tool_calls": [asdict(call) for call in scenario.expected_tool_calls],
        "success_criteria": scenario.success_criteria,
        "tags": scenario.tags,
    }


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
