from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


class ToolExecutionError(RuntimeError):
    pass


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., dict[str, Any]]


INVENTORY = {
    "HTF7000-FUEL-NOZZLE": {"on_hand": 22, "lead_days": 21, "approved_alternates": ["HN-7000-A"], "constraint": "qualified_supplier_only"},
    "APU-CONTROL-UNIT": {"on_hand": 3, "lead_days": 65, "approved_alternates": ["APU-CU-R2"], "constraint": "software_load_verification"},
    "TITANIUM-BRACKET-42": {"on_hand": 0, "lead_days": 45, "approved_alternates": ["TB-42-ALT"], "constraint": "material_cert_required"},
    "ACTUATOR-SEAL-KIT": {"on_hand": 61, "lead_days": 9, "approved_alternates": [], "constraint": "batch_traceability"},
    "CABIN-PRESSURE-SENSOR": {"on_hand": 8, "lead_days": 34, "approved_alternates": ["CPS-88B"], "constraint": "dual_release_required"},
    "FADEC-MEMORY-MODULE": {"on_hand": 5, "lead_days": 72, "approved_alternates": [], "constraint": "export_review_required"},
}

SUPPLIERS = {
    "HN-7000-A": {"supplier": "Northstar Components", "status": "approved", "quality_score": 0.98, "region": "US"},
    "APU-CU-R2": {"supplier": "AeroLogic Systems", "status": "conditional", "quality_score": 0.91, "region": "US"},
    "TB-42-ALT": {"supplier": "Vector Forge", "status": "approved", "quality_score": 0.96, "region": "US"},
    "CPS-88B": {"supplier": "Helio Avionics", "status": "approved", "quality_score": 0.94, "region": "EU"},
}

REGULATORY = {
    "itar_export_review": {"finding": "Export review is required before sharing controlled technical data.", "authority": "synthetic-export-control-policy", "escalate": True},
    "faa_pma_repair": {"finding": "PMA substitution requires approved eligibility evidence and repair station traceability.", "authority": "synthetic-faa-airworthiness-note", "escalate": False},
    "cmmc_supplier_data": {"finding": "Supplier data exchange must use approved controlled-information handling.", "authority": "synthetic-cmmc-control-family", "escalate": True},
    "easa_dual_release": {"finding": "Dual release evidence is required before EU-to-US acceptance.", "authority": "synthetic-easa-release-procedure", "escalate": False},
    "safety_critical_change": {"finding": "Safety-critical recommendations need human approval and rationale capture.", "authority": "synthetic-safety-governance-standard", "escalate": True},
}


def part_inventory(part_number: str) -> dict[str, Any]:
    item = INVENTORY.get(part_number)
    if not item:
        return {"part_number": part_number, "status": "unknown", "on_hand": 0, "lead_days": None}
    return {"part_number": part_number, "status": "known", **item}


def supplier_lookup(part_number: str, alternate_part: str | None = None) -> dict[str, Any]:
    inventory = INVENTORY.get(part_number, {})
    candidate = alternate_part or next(iter(inventory.get("approved_alternates", [])), "")
    supplier = SUPPLIERS.get(candidate)
    if not supplier:
        return {"part_number": part_number, "alternate_part": candidate, "status": "no_approved_supplier"}
    return {"part_number": part_number, "alternate_part": candidate, **supplier}


def expedite_options(part_number: str, required_days: int) -> dict[str, Any]:
    inventory = INVENTORY.get(part_number, {})
    lead_days = inventory.get("lead_days") or 999
    expedite_days = max(7, int(lead_days * 0.45))
    feasible = expedite_days <= required_days
    return {
        "part_number": part_number,
        "standard_lead_days": lead_days,
        "expedite_days": expedite_days,
        "feasible": feasible,
        "tradeoff": "premium freight and supplier capacity review",
    }


def regulatory_lookup(topic: str, jurisdiction: str = "US") -> dict[str, Any]:
    finding = REGULATORY.get(topic)
    if not finding:
        return {"topic": topic, "jurisdiction": jurisdiction, "finding": "No synthetic policy match.", "escalate": True}
    return {"topic": topic, "jurisdiction": jurisdiction, **finding}


def bid_risk_model(program: str, margin_percent: float, compliance_risk: str, supply_risk: str) -> dict[str, Any]:
    risk_weights = {"low": 0.1, "medium": 0.28, "high": 0.55}
    risk_penalty = risk_weights.get(compliance_risk, 0.55) + risk_weights.get(supply_risk, 0.55)
    adjusted_margin = round(margin_percent - (risk_penalty * 10), 2)
    recommendation = "bid" if adjusted_margin >= 12 and compliance_risk != "high" else "conditional_bid"
    if adjusted_margin < 8 or compliance_risk == "high":
        recommendation = "no_bid_or_exec_review"
    return {
        "program": program,
        "margin_percent": margin_percent,
        "adjusted_margin": adjusted_margin,
        "compliance_risk": compliance_risk,
        "supply_risk": supply_risk,
        "recommendation": recommendation,
    }


TOOL_DEFINITIONS: dict[str, ToolDefinition] = {
    "part_inventory": ToolDefinition(
        name="part_inventory",
        description="Lookup synthetic inventory, lead time, and qualification constraints for an aerospace part.",
        input_schema={
            "type": "object",
            "properties": {"part_number": {"type": "string"}},
            "required": ["part_number"],
        },
        handler=part_inventory,
    ),
    "supplier_lookup": ToolDefinition(
        name="supplier_lookup",
        description="Lookup approved or conditional alternate supplier status for a part.",
        input_schema={
            "type": "object",
            "properties": {
                "part_number": {"type": "string"},
                "alternate_part": {"type": "string"},
            },
            "required": ["part_number"],
        },
        handler=supplier_lookup,
    ),
    "expedite_options": ToolDefinition(
        name="expedite_options",
        description="Evaluate whether an expedited supply path can meet a required timeline.",
        input_schema={
            "type": "object",
            "properties": {
                "part_number": {"type": "string"},
                "required_days": {"type": "integer"},
            },
            "required": ["part_number", "required_days"],
        },
        handler=expedite_options,
    ),
    "regulatory_lookup": ToolDefinition(
        name="regulatory_lookup",
        description="Retrieve synthetic regulatory or governance findings for industrial AI workflows.",
        input_schema={
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "jurisdiction": {"type": "string"},
            },
            "required": ["topic"],
        },
        handler=regulatory_lookup,
    ),
    "bid_risk_model": ToolDefinition(
        name="bid_risk_model",
        description="Calculate risk-adjusted bid posture using synthetic margin, compliance, and supply risk inputs.",
        input_schema={
            "type": "object",
            "properties": {
                "program": {"type": "string"},
                "margin_percent": {"type": "number"},
                "compliance_risk": {"type": "string", "enum": ["low", "medium", "high"]},
                "supply_risk": {"type": "string", "enum": ["low", "medium", "high"]},
            },
            "required": ["program", "margin_percent", "compliance_risk", "supply_risk"],
        },
        handler=bid_risk_model,
    ),
}

TOOL_SCHEMAS = [
    {
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.input_schema,
    }
    for tool in TOOL_DEFINITIONS.values()
]


def execute_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    definition = TOOL_DEFINITIONS.get(name)
    if definition is None:
        raise ToolExecutionError(f"Unknown tool: {name}")
    return definition.handler(**args)
