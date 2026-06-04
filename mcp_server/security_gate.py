from typing import Callable

from classifier.incident_classifier import classify_incident_as_dict
from security.prompt_guard import evaluate_security
from security.security_response import build_blocked_security_response


def handle_security_gate(
    user_input: str,
    rag_runner: Callable[[], object] | None = None,
    graph_runner: Callable[[], object] | None = None,
    planner_runner: Callable[[], object] | None = None,
) -> dict:
    decision = evaluate_security(user_input)
    if decision.status == "blocked":
        return build_blocked_security_response(decision)

    if rag_runner is not None:
        rag_runner()
    if graph_runner is not None:
        graph_runner()
    if planner_runner is not None:
        planner_runner()

    return {"status": "allowed"}


def handle_entry_gate(
    user_input: str,
    rag_runner: Callable[[], object] | None = None,
    graph_runner: Callable[[], object] | None = None,
    planner_runner: Callable[[], object] | None = None,
) -> dict:
    decision = evaluate_security(user_input)
    if decision.status == "blocked":
        return build_blocked_security_response(decision)

    classification = classify_incident_as_dict(user_input)

    if rag_runner is not None:
        rag_runner()
    if graph_runner is not None:
        graph_runner()
    if planner_runner is not None:
        planner_runner()

    return {
        "status": "allowed",
        "classification": classification,
    }
