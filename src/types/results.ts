export interface BenchmarkSummary {
  generated_at: string;
  benchmark: {
    name: string;
    version: string;
    scenario_count: number;
    agent_count: number;
    categories: string[];
    metric_weights: Record<string, number>;
  };
  leaderboard: LeaderboardRow[];
  scenario_results: ScenarioResult[];
  scenarios: PublicScenario[];
}

export interface LeaderboardRow {
  agent: string;
  scenario_count: number;
  composite_score: number;
  task_completion: number;
  tool_call_accuracy: number;
  loop_termination: number;
  grounding: number;
  governance: number;
  hallucination_rate: number;
}

export interface PublicScenario {
  id: string;
  title: string;
  category: string;
  risk_level: "high" | "low" | "medium";
  prompt: string;
  max_steps: number;
  allowed_tools: string[];
  expected_tool_calls: Array<{
    name: string;
    args: Record<string, unknown>;
  }>;
  success_criteria: string[];
  tags: string[];
}

export interface ScenarioResult {
  agent: string;
  scenario_id: string;
  composite_score: number;
  metrics: Record<
    string,
    {
      name: string;
      score: number;
      passed: boolean;
      rationale: string;
    }
  >;
  tool_calls: Array<{
    name: string;
    args: Record<string, unknown>;
    result: Record<string, unknown>;
  }>;
  terminated: boolean;
  steps: number;
  final_answer: string;
}
