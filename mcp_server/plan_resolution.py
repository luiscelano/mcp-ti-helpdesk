from pathlib import Path
from typing import Sequence

from planner.backward_chaining import (
    build_backward_chaining_plan,
    validate_plan_execution,
)


def plan_resolution_tool(
    goal_fact: str | None = None,
    initial_facts: Sequence[str] | None = None,
    plan: Sequence[str] | None = None,
    source_path: str | Path = "data/archivo3_acciones.json",
) -> dict:
    if plan is not None:
        validation = validate_plan_execution(
            plan=plan,
            initial_facts=initial_facts,
            source_path=source_path,
        )
        return {
            "tool": "plan_resolution",
            "status": "ok",
            "mode": "validate",
            "goal": goal_fact,
            "parameters": {
                "initial_facts": list(initial_facts) if initial_facts is not None else [],
                "source_path": str(source_path),
            },
            "resolution_plan": list(plan),
            "plan_ids": [],
            "total_cost": 0,
            "is_valid": validation["is_valid"],
            "validation": validation,
        }

    if goal_fact is None:
        raise ValueError("goal_fact is required when plan is not provided")

    result = build_backward_chaining_plan(
        goal_fact=goal_fact,
        initial_facts=initial_facts,
        source_path=source_path,
    )
    validation = validate_plan_execution(
        plan=result["plan"],
        initial_facts=initial_facts,
        source_path=source_path,
    )

    return {
        "tool": "plan_resolution",
        "status": "ok",
        "mode": "plan",
        "goal": result["goal"],
        "parameters": {
            "initial_facts": result["initial_facts"],
            "source_path": str(source_path),
        },
        "resolution_plan": result["plan"],
        "plan_ids": result["plan_ids"],
        "total_cost": result["total_cost"],
        "is_valid": result["is_valid"] and validation["is_valid"],
        "validation": validation,
        "final_facts": result["final_facts"],
    }