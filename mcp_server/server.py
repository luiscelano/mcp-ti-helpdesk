from mcp.server.fastmcp import FastMCP

from mcp_server.document_search import search_documents_tool
from mcp_server.graph_search import search_graph_tool
from mcp_server.plan_resolution import plan_resolution_tool
from mcp_server.resolve_incident import resolve_incident_tool

mcp = FastMCP("mcp-ti-helpdesk")


@mcp.tool()
def resolve_incident(incident: str) -> dict:
    return resolve_incident_tool(incident)


@mcp.tool()
def search_documents(
    query: str,
    top_k: int = 3,
    persist_dir: str = ".chroma",
    category_filters: list[str] | None = None,
) -> dict:
    return search_documents_tool(
        query=query,
        top_k=top_k,
        persist_dir=persist_dir,
        category_filters=category_filters,
    )


@mcp.tool()
def search_graph(node_name: str, depth: int = 2) -> dict:
    return search_graph_tool(node_name=node_name, depth=depth)


@mcp.tool()
def plan_resolution(
    goal_fact: str | None = None,
    initial_facts: list[str] | None = None,
    plan: list[str] | None = None,
    source_path: str = "data/archivo3_acciones.json",
) -> dict:
    return plan_resolution_tool(
        goal_fact=goal_fact,
        initial_facts=initial_facts,
        plan=plan,
        source_path=source_path,
    )


def run_stdio_server() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run_stdio_server()
