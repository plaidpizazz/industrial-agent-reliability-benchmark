from agenteval import load_scenarios
from agenteval.tools.registry import TOOL_DEFINITIONS


def test_scenario_dataset_has_expected_shape() -> None:
    scenarios = load_scenarios()
    assert len(scenarios) == 18
    assert len({scenario.id for scenario in scenarios}) == len(scenarios)
    assert {scenario.category for scenario in scenarios} == {"bid_no_bid", "regulatory", "supply_chain"}


def test_scenarios_reference_known_tools() -> None:
    known_tools = set(TOOL_DEFINITIONS)
    for scenario in load_scenarios():
        assert set(scenario.allowed_tools).issubset(known_tools)
        assert {call.name for call in scenario.expected_tool_calls}.issubset(set(scenario.allowed_tools))
        assert scenario.max_steps >= len(scenario.expected_tool_calls) + 1
