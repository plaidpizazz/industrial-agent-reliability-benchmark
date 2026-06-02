from __future__ import annotations

import json
from pathlib import Path

from .schemas import Scenario

DEFAULT_SCENARIO_PATH = Path(__file__).resolve().parents[2] / "scenarios" / "aerospace_synthetic_v0.jsonl"


def load_scenarios(path: str | Path = DEFAULT_SCENARIO_PATH) -> list[Scenario]:
    scenario_path = Path(path)
    scenarios: list[Scenario] = []
    with scenario_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                scenarios.append(Scenario.from_dict(json.loads(stripped)))
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"Invalid scenario at {scenario_path}:{line_number}: {exc}") from exc
    return scenarios


def to_huggingface_dataset(scenarios: list[Scenario]):
    try:
        from datasets import Dataset
    except ImportError as exc:
        raise RuntimeError("Install the datasets package to export a Hugging Face Dataset") from exc

    return Dataset.from_list([scenario.to_dict() for scenario in scenarios])
