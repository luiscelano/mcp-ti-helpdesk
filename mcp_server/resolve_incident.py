from pathlib import Path
from typing import Callable, Sequence

from classifier.incident_classifier import classify_incident_as_dict
from mcp_server.document_search import search_documents_tool
from mcp_server.graph_search import search_graph_tool
from mcp_server.plan_resolution import plan_resolution_tool
from mcp_server.response_generator import build_structured_response
from security.prompt_guard import evaluate_security
from security.security_response import build_blocked_security_response


def _extract_result_ids(results: Sequence[object]) -> list[str]:
    extracted: list[str] = []
    for result in results:
        if isinstance(result, dict) and "id" in result:
            extracted.append(str(result["id"]))
        else:
            extracted.append(str(result))
    return extracted


def _select_graph_node(category: str) -> str:
    if category == "acceso":
        return "AccesoBloqueado"
    return "AccesoBloqueado"


def _select_plan_goal(category: str) -> str:
    if category == "acceso":
        return "usuario_desbloqueado"
    return "usuario_desbloqueado"


def _record_stage_error(stage_errors: list[dict], stage: str, error: Exception) -> None:
    stage_errors.append(
        {
            "stage": stage,
            "error_type": error.__class__.__name__,
            "message": str(error),
        }
    )


def resolve_incident_tool(
    incident: str,
    *,
    security_checker: Callable[[str], object] = evaluate_security,
    classifier: Callable[[str], dict] = classify_incident_as_dict,
    document_tool: Callable[..., dict] = search_documents_tool,
    graph_tool: Callable[..., dict] = search_graph_tool,
    plan_tool: Callable[..., dict] = plan_resolution_tool,
    document_top_k: int = 3,
    graph_depth: int = 2,
    rag_category_filters: Sequence[str] | None = None,
    plan_source_path: str | Path = "data/archivo3_acciones.json",
) -> dict:
    stage_errors: list[dict] = []

    security_decision = security_checker(incident)
    if getattr(security_decision, "status", None) == "blocked":
        return build_blocked_security_response(security_decision)

    try:
        classification = classifier(incident)
    except Exception as error:
        _record_stage_error(stage_errors, "classification", error)
        classification = {"category": "desconocido"}

    category = str(classification.get("category", "desconocido"))
    category_filters = list(rag_category_filters) if rag_category_filters is not None else [category]

    rag_results: list[str] = []
    try:
        rag_response = document_tool(
            query=incident,
            top_k=document_top_k,
            persist_dir=".chroma",
            category_filters=category_filters,
        )
        rag_results = _extract_result_ids(rag_response.get("results", []))
    except Exception as error:
        _record_stage_error(stage_errors, "rag", error)

    graph_results: list[str] = []
    try:
        graph_response = graph_tool(
            node_name=_select_graph_node(category),
            depth=graph_depth,
        )
        graph_results = [str(result) for result in graph_response.get("results", [])]
    except Exception as error:
        _record_stage_error(stage_errors, "graph", error)

    resolution_plan: list[str] = []
    try:
        plan_response = plan_tool(
            goal_fact=_select_plan_goal(category),
            source_path=plan_source_path,
        )
        resolution_plan = [str(action) for action in plan_response.get("resolution_plan", [])]
    except Exception as error:
        _record_stage_error(stage_errors, "planner", error)

    return build_structured_response(
        classification=classification,
        rag_results=rag_results,
        graph_results=graph_results,
        resolution_plan=resolution_plan,
        stage_errors=stage_errors,
    )
