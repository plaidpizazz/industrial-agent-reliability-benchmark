import summary from "../../public/results/benchmark-summary.json";
import type { BenchmarkSummary, ScenarioResult } from "@/types/results";

export const benchmarkSummary = summary as BenchmarkSummary;

const reference = benchmarkSummary.leaderboard[0];

export const metricRows = [
  { label: "Task completion", value: reference.task_completion },
  { label: "Tool-call accuracy", value: reference.tool_call_accuracy },
  { label: "Grounding", value: reference.grounding },
  { label: "Governance", value: reference.governance },
];

export const categorySummaries = benchmarkSummary.scenarios.map((scenario) => scenario.category).reduce(
  (accumulator, category) => {
    if (!accumulator.some((entry) => entry.name === category)) {
      const categoryScenarios = benchmarkSummary.scenarios.filter((scenario) => scenario.category === category);
      accumulator.push({
        name: category,
        count: categoryScenarios.length,
        risks: Array.from(new Set(categoryScenarios.map((scenario) => scenario.risk_level))).sort(),
      });
    }
    return accumulator;
  },
  [] as Array<{ name: string; count: number; risks: string[] }>,
);

export const failureExamples = benchmarkSummary.scenario_results
  .filter((result: ScenarioResult) => result.agent === "FlawedAgent")
  .sort((left, right) => left.composite_score - right.composite_score)
  .slice(0, 3);
