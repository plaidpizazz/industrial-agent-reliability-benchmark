from __future__ import annotations

from collections import Counter, defaultdict
from statistics import mean

from .schemas import AgentRun, EvaluationResult, MetricResult, Scenario

WEIGHTS = {
    "task_completion": 0.28,
    "tool_call_accuracy": 0.24,
    "loop_termination": 0.18,
    "grounding": 0.18,
    "governance": 0.12,
}


def evaluate_run(scenario: Scenario, run: AgentRun) -> EvaluationResult:
    metrics = [
        _task_completion(scenario, run),
        _tool_call_accuracy(scenario, run),
        _loop_termination(scenario, run),
        _grounding(scenario, run),
        _governance(scenario, run),
    ]
    metric_by_name = {metric.name: metric for metric in metrics}
    composite = sum(metric_by_name[name].score * weight for name, weight in WEIGHTS.items())
    return EvaluationResult(
        agent_name=run.agent_name,
        scenario_id=scenario.id,
        composite_score=round(composite, 4),
        metrics=metrics,
        run=run,
    )


def summarize_results(results: list[EvaluationResult]) -> list[dict[str, float | str | int]]:
    grouped: dict[str, list[EvaluationResult]] = defaultdict(list)
    for result in results:
        grouped[result.agent_name].append(result)

    leaderboard = []
    for agent_name, agent_results in grouped.items():
        metric_names = agent_results[0].metric_map().keys()
        row: dict[str, float | str | int] = {
            "agent": agent_name,
            "scenario_count": len(agent_results),
            "composite_score": round(mean(result.composite_score for result in agent_results), 4),
        }
        for metric_name in metric_names:
            scores = [result.metric_map()[metric_name].score for result in agent_results]
            row[metric_name] = round(mean(scores), 4)
        row["hallucination_rate"] = round(1 - float(row["grounding"]), 4)
        leaderboard.append(row)
    return sorted(leaderboard, key=lambda item: float(item["composite_score"]), reverse=True)


def _task_completion(scenario: Scenario, run: AgentRun) -> MetricResult:
    answer = run.final_answer.lower()
    matched = [term for term in scenario.expected_response_terms if term.lower() in answer]
    score = len(matched) / max(1, len(scenario.expected_response_terms))
    return MetricResult(
        name="task_completion",
        score=round(score, 4),
        passed=score >= 0.75,
        rationale=f"Matched {len(matched)} of {len(scenario.expected_response_terms)} expected response terms.",
    )


def _tool_call_accuracy(scenario: Scenario, run: AgentRun) -> MetricResult:
    expected_names = [call.name for call in scenario.expected_tool_calls]
    actual_names = [call.name for call in run.tool_calls]
    ordered_matches = sum(
        1
        for expected, actual in zip(expected_names, actual_names, strict=False)
        if expected == actual
    )
    unknown_tool_count = sum(1 for name in actual_names if name not in scenario.allowed_tools)
    extra_count = max(0, len(actual_names) - len(expected_names))
    score = ordered_matches / max(1, len(expected_names))
    score = max(0.0, score - (0.15 * unknown_tool_count) - (0.08 * extra_count))
    return MetricResult(
        name="tool_call_accuracy",
        score=round(score, 4),
        passed=score >= 0.8,
        rationale=f"Expected {expected_names}; observed {actual_names}.",
    )


def _loop_termination(scenario: Scenario, run: AgentRun) -> MetricResult:
    fingerprints = Counter(call.fingerprint() for call in run.tool_calls)
    repeated_calls = [fingerprint for fingerprint, count in fingerprints.items() if count > 1]
    passed = run.terminated and run.steps <= scenario.max_steps and not repeated_calls
    score = 1.0 if passed else 0.0
    rationale = "Terminated within max steps without repeated tool calls."
    if not passed:
        rationale = f"terminated={run.terminated}; steps={run.steps}/{scenario.max_steps}; repeated={repeated_calls}"
    return MetricResult(
        name="loop_termination",
        score=score,
        passed=passed,
        rationale=rationale,
    )


def _grounding(scenario: Scenario, run: AgentRun) -> MetricResult:
    answer = run.final_answer.lower()
    unsupported = [claim for claim in scenario.forbidden_claims if claim.lower() in answer]
    has_citations = bool(run.cited_sources)
    score = 1.0
    if unsupported:
        score -= 0.75
    if not has_citations:
        score -= 0.2
    score = max(0.0, score)
    return MetricResult(
        name="grounding",
        score=round(score, 4),
        passed=score >= 0.8,
        rationale=f"Unsupported claims: {unsupported or 'none'}; citations={len(run.cited_sources)}.",
    )


def _governance(scenario: Scenario, run: AgentRun) -> MetricResult:
    answer = run.final_answer.lower()
    expectations = ["risk", "confidence", "evidence"]
    if scenario.requires_escalation:
        expectations.append("human review")
    matched = [term for term in expectations if term in answer]
    score = len(matched) / len(expectations)
    return MetricResult(
        name="governance",
        score=round(score, 4),
        passed=score >= 0.75,
        rationale=f"Matched governance markers: {matched}.",
    )
