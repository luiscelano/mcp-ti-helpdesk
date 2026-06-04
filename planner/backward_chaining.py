from __future__ import annotations

from pathlib import Path
from typing import Sequence

from planner.action_catalog import ActionCatalog


def _normalize_facts(facts: Sequence[str] | None) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    if facts is None:
        return normalized

    for fact in facts:
        fact_name = str(fact).strip()
        if not fact_name or fact_name in seen:
            continue
        seen.add(fact_name)
        normalized.append(fact_name)

    return normalized


def _resolve_goal(
    goal_fact: str,
    catalog: ActionCatalog,
    known_facts: set[str],
    visiting: set[str],
) -> tuple[list[object], set[str], int]:
    if goal_fact in known_facts:
        return [], set(known_facts), 0

    candidates = catalog.actions_for_effect(goal_fact)
    if not candidates:
        raise ValueError(f"No action can produce goal fact: {goal_fact}")

    best_plan: list[object] | None = None
    best_facts: set[str] | None = None
    best_cost: int | None = None

    for action in sorted(candidates, key=lambda candidate: (candidate.costo_minutos, candidate.nombre)):
        if action.nombre in visiting:
            continue

        candidate_facts = set(known_facts)
        candidate_plan: list[object] = []
        candidate_cost = 0
        candidate_visiting = set(visiting)
        candidate_visiting.add(action.nombre)

        try:
            for precondition in action.precondiciones:
                if precondition not in candidate_facts:
                    sub_plan, candidate_facts, sub_cost = _resolve_goal(
                        precondition,
                        catalog,
                        candidate_facts,
                        candidate_visiting,
                    )
                    candidate_plan.extend(sub_plan)
                    candidate_cost += sub_cost

            candidate_plan.append(action)
            candidate_facts.update(action.efectos)
            candidate_cost += action.costo_minutos
        except ValueError:
            continue

        if best_plan is None or candidate_cost < best_cost or (
            candidate_cost == best_cost and [step.nombre for step in candidate_plan] < [step.nombre for step in best_plan]
        ):
            best_plan = candidate_plan
            best_facts = candidate_facts
            best_cost = candidate_cost

    if best_plan is None or best_facts is None or best_cost is None:
        raise ValueError(f"No valid backward chaining plan found for goal: {goal_fact}")

    return best_plan, best_facts, best_cost


def build_backward_chaining_plan(
    goal_fact: str,
    initial_facts: Sequence[str] | None = None,
    source_path: str | Path = "data/archivo3_acciones.json",
) -> dict:
    catalog = ActionCatalog.from_json(str(source_path))
    return build_backward_chaining_plan_from_catalog(goal_fact, catalog, initial_facts)


def build_backward_chaining_plan_from_catalog(
    goal_fact: str,
    catalog: ActionCatalog,
    initial_facts: Sequence[str] | None = None,
) -> dict:
    facts = set(_normalize_facts(initial_facts))
    plan, final_facts, total_cost = _resolve_goal(goal_fact, catalog, facts, set())

    return {
        "goal": goal_fact,
        "initial_facts": _normalize_facts(initial_facts),
        "plan": [action.nombre for action in plan],
        "plan_ids": [action.id for action in plan],
        "total_cost": total_cost,
        "final_facts": sorted(final_facts),
        "is_valid": True,
    }


def plan_is_valid(
    plan: Sequence[str],
    initial_facts: Sequence[str] | None = None,
    catalog: ActionCatalog | None = None,
    source_path: str | Path = "data/archivo3_acciones.json",
) -> bool:
    if catalog is None:
        catalog = ActionCatalog.from_json(str(source_path))
    known_facts = set(_normalize_facts(initial_facts))

    for action_name in plan:
        action = catalog.get_action(action_name)
        if not set(action.precondiciones).issubset(known_facts):
            return False
        known_facts.update(action.efectos)

    return True


def validate_plan_execution(
    plan: Sequence[str],
    initial_facts: Sequence[str] | None = None,
    catalog: ActionCatalog | None = None,
    source_path: str | Path = "data/archivo3_acciones.json",
) -> dict:
    if catalog is None:
        catalog = ActionCatalog.from_json(str(source_path))
    known_facts = set(_normalize_facts(initial_facts))
    executed_actions: list[str] = []

    for action_name in plan:
        action = catalog.get_action(action_name)
        missing_preconditions = [
            precondition for precondition in action.precondiciones if precondition not in known_facts
        ]
        if missing_preconditions:
            return {
                "is_valid": False,
                "executed_actions": executed_actions,
                "blocked_action": action.nombre,
                "missing_preconditions": missing_preconditions,
                "known_facts": sorted(known_facts),
            }

        executed_actions.append(action.nombre)
        known_facts.update(action.efectos)

    return {
        "is_valid": True,
        "executed_actions": executed_actions,
        "blocked_action": None,
        "missing_preconditions": [],
        "known_facts": sorted(known_facts),
    }