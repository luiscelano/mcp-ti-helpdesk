from pathlib import Path
from typing import Dict, List, Sequence

import chromadb

from rag.chroma_indexer import index_documents_no_chunking
from rag.embedding import HelpdeskEmbeddingFunction


DEFAULT_COLLECTION_NAME = "ti_helpdesk_documents_semantic"
DEFAULT_TOP_K = 3


def _normalize_top_k(top_k: int) -> int:
    return max(1, min(top_k, 4))


def _normalize_where(category_filters: Sequence[str] | None) -> dict | None:
    if not category_filters:
        return None

    normalized = [value.strip() for value in category_filters if value.strip()]
    if not normalized:
        return None
    if len(normalized) == 1:
        return {"categoria": normalized[0]}
    return {"$or": [{"categoria": value} for value in normalized]}


def search_documents(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    persist_dir: str | Path = ".chroma",
    collection_name: str = DEFAULT_COLLECTION_NAME,
    category_filters: Sequence[str] | None = None,
) -> Dict[str, object]:
    embedding_function = HelpdeskEmbeddingFunction()
    normalized_top_k = _normalize_top_k(top_k)
    where_clause = _normalize_where(category_filters)

    index_documents_no_chunking(
        persist_dir=persist_dir,
        collection_name=collection_name,
        embedding_function=embedding_function,
    )

    client = chromadb.PersistentClient(path=str(persist_dir))
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function,
        metadata={"indexing_strategy": "no_chunking"},
    )

    raw = collection.query(
        query_texts=[query],
        n_results=normalized_top_k,
        include=["documents", "metadatas", "distances"],
        where=where_clause,
    )

    ids = raw.get("ids", [[]])[0]
    documents = raw.get("documents", [[]])[0]
    metadatas = raw.get("metadatas", [[]])[0]
    distances = raw.get("distances", [[]])[0]

    results: List[Dict[str, object]] = []
    for doc_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
        results.append(
            {
                "id": doc_id,
                "document": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    # Keep ordering deterministic when distances tie.
    results.sort(key=lambda item: (float(item["distance"]), str(item["id"])))

    return {
        "query": query,
        "top_k": normalized_top_k,
        "category_filters": list(category_filters or []),
        "results": results,
    }