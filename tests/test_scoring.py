from agenteval import FlawedAgentRunner, ReferenceAgentRunner, evaluate_run, load_scenarios, summarize_results


def test_reference_agent_clears_reliability_gate() -> None:
    scenarios = load_scenarios()
    runner = ReferenceAgentRunner()
    results = [evaluate_run(scenario, runner.run(scenario)) for scenario in scenarios]
    leaderboard = summarize_results(results)
    assert leaderboard[0]["composite_score"] >= 0.92
    assert leaderboard[0]["tool_call_accuracy"] == 1.0
    assert leaderboard[0]["loop_termination"] == 1.0


def test_flawed_agent_is_caught_by_evaluators() -> None:
    scenarios = load_scenarios()
    reference = [evaluate_run(scenario, ReferenceAgentRunner().run(scenario)) for scenario in scenarios]
    flawed = [evaluate_run(scenario, FlawedAgentRunner().run(scenario)) for scenario in scenarios]
    reference_score = summarize_results(reference)[0]["composite_score"]
    flawed_score = summarize_results(flawed)[0]["composite_score"]
    assert flawed_score < reference_score
    assert flawed_score < 0.65
