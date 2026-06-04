from dataclasses import asdict, dataclass

from security.prompt_guard import SecurityDecision


@dataclass(frozen=True)
class BlockedSecurityResponse:
    status: str
    reason: str
    classification: dict
    rag_results: list
    graph_results: list
    resolution_plan: list


def build_blocked_security_response(decision: SecurityDecision) -> dict:
    if decision.status != "blocked" or not decision.reason:
        raise ValueError("Blocked security response requires a blocked decision with reason")

    response = BlockedSecurityResponse(
        status="blocked",
        reason=decision.reason,
        classification={},
        rag_results=[],
        graph_results=[],
        resolution_plan=[],
    )
    return asdict(response)
