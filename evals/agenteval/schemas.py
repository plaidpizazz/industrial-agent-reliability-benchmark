from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

RiskLevel = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class ExpectedToolCall:
    name: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Scenario:
    id: str
    title: str
    category: str
    risk_level: RiskLevel
    prompt: str
    max_steps: int
    allowed_tools: list[str]
    expected_tool_calls: list[ExpectedToolCall]
    reference_facts: list[str]
    expected_response_terms: list[str]
    forbidden_claims: list[str]
    requires_escalation: bool
    success_criteria: list[str]
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Scenario":
        expected = [
            ExpectedToolCall(name=item["name"], args=item.get("args", {}))
            for item in data["expected_tool_calls"]
        ]
        return cls(
            id=data["id"],
            title=data["title"],
            category=data["category"],
            risk_level=data["risk_level"],
            prompt=data["prompt"],
            max_steps=int(data["max_steps"]),
            allowed_tools=list(data["allowed_tools"]),
            expected_tool_calls=expected,
            reference_facts=list(data["reference_facts"]),
            expected_response_terms=list(data["expected_response_terms"]),
            forbidden_claims=list(data["forbidden_claims"]),
            requires_escalation=bool(data["requires_escalation"]),
            success_criteria=list(data["success_criteria"]),
            tags=list(data.get("tags", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ToolCall:
    name: str
    args: dict[str, Any]
    result: dict[str, Any]

    def fingerprint(self) -> str:
        args = ",".join(f"{key}={self.args[key]}" for key in sorted(self.args))
        return f"{self.name}({args})"


@dataclass(frozen=True)
class AgentRun:
    agent_name: str
    scenario_id: str
    final_answer: str
    tool_calls: list[ToolCall]
    terminated: bool
    steps: int
    cited_sources: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MetricResult:
    name: str
    score: float
    passed: bool
    rationale: str


@dataclass(frozen=True)
class EvaluationResult:
    agent_name: str
    scenario_id: str
    composite_score: float
    metrics: list[MetricResult]
    run: AgentRun

    def metric_map(self) -> dict[str, MetricResult]:
        return {metric.name: metric for metric in self.metrics}

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
