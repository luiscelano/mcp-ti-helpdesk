from __future__ import annotations


def build_final_response(
    classification: dict,
    rag_results: list[str],
    graph_results: list[str],
    resolution_plan: list[str],
) -> str:
    category = str(classification.get("category", "desconocido"))
    rag_summary = ", ".join(rag_results) if rag_results else "sin coincidencias"
    graph_summary = ", ".join(graph_results) if graph_results else "sin relaciones"
    plan_summary = ", ".join(resolution_plan) if resolution_plan else "sin plan"
    return (
        f"Incidente clasificado como {category}. "
        f"RAG: {rag_summary}. "
        f"GraphRAG: {graph_summary}. "
        f"Plan: {plan_summary}."
    )


def build_structured_response(
    classification: dict,
    rag_results: list[str],
    graph_results: list[str],
    resolution_plan: list[str],
    stage_errors: list[dict] | None = None,
) -> dict:
    traced_errors = list(stage_errors) if stage_errors is not None else []
    final_response = build_final_response(
        classification=classification,
        rag_results=rag_results,
        graph_results=graph_results,
        resolution_plan=resolution_plan,
    )

    if traced_errors:
        warnings = "; ".join(
            f"{entry['stage']}: {entry['message']}" for entry in traced_errors
        )
        final_response = f"{final_response} Advertencias: {warnings}."

    return {
        "status": "allowed",
        "classification": classification,
        "rag_results": rag_results,
        "graph_results": graph_results,
        "resolution_plan": resolution_plan,
        "final_response": final_response,
        "stage_errors": traced_errors,
    }