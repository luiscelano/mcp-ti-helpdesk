from graph_rag.search_graph import format_graph_response, search_graph


def search_graph_tool(node_name: str, depth: int = 2) -> dict:
    result = search_graph(node_name=node_name, depth=depth)
    return {
        "tool": "search_graph",
        "status": "ok",
        "query": result["query"],
        "parameters": {
            "depth": depth,
        },
        "results": format_graph_response(result),
        "direct_relations": result["direct_relations"],
        "two_hop_paths": result["two_hop_paths"],
        "result_count": len(format_graph_response(result)),
    }
