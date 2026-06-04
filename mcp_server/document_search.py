from pathlib import Path
from typing import Sequence

from rag.search_documents import search_documents


def search_documents_tool(
    query: str,
    top_k: int = 3,
    persist_dir: str | Path = ".chroma",
    category_filters: Sequence[str] | None = None,
) -> dict:
    result = search_documents(
        query=query,
        top_k=top_k,
        persist_dir=persist_dir,
        category_filters=category_filters,
    )

    return {
        "tool": "search_documents",
        "status": "ok",
        "query": result["query"],
        "parameters": {
            "top_k": result["top_k"],
            "category_filters": result["category_filters"],
        },
        "results": result["results"],
        "result_count": len(result["results"]),
    }