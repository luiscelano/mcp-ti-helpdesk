from pathlib import Path
from typing import Dict, Optional

from ingestion.ingest_documents import REQUIRED_DOCUMENT_IDS, process_documents
from ingestion.load_actions import load_actions
from ingestion.load_graph import load_graph_from_csv, run_graph_validation_queries
from rag.chroma_indexer import index_documents_no_chunking


class _FakeEmbeddingFunction:
    def __call__(self, input):
        return [[0.0, 0.0, 0.0] for _ in input]

    def name(self) -> str:
        return "ingest-e2e-fake"

    def is_legacy(self) -> bool:
        return False

    def default_space(self) -> str:
        return "cosine"

    def supported_spaces(self):
        return ["cosine", "l2", "ip"]


def run_ingest_end_to_end(
    doc_source: str | Path = "data/archivo1_documentos.json",
    graph_source: str | Path = "data/archivo2_grafo.csv",
    actions_source: str | Path = "data/archivo3_acciones.json",
    persist_dir: str | Path = ".chroma",
    collection_name: str = "ti_helpdesk_documents_ingest_e2e",
    embedding_function: Optional[object] = None,
) -> Dict[str, bool]:
    docs = process_documents(doc_source)
    doc_ids = {str(doc["id"]) for doc in docs}
    ingest_001_ok = doc_ids == set(REQUIRED_DOCUMENT_IDS)

    index_result = index_documents_no_chunking(
        source_path=doc_source,
        persist_dir=persist_dir,
        collection_name=collection_name,
        embedding_function=embedding_function or _FakeEmbeddingFunction(),
    )
    ingest_002_ok = (
        index_result["indexed_count"] == 4
        and set(index_result["indexed_ids"]) == set(REQUIRED_DOCUMENT_IDS)
    )

    graph_result = load_graph_from_csv(graph_source)
    graph_validation = run_graph_validation_queries()
    ingest_graph_ok = graph_result["relationships_loaded"] >= 9 and all(
        graph_validation.values()
    )

    actions = load_actions(actions_source)
    ingest_003_ok = len(actions) >= 1 and all(action.efectos for action in actions)

    return {
        "INGEST-001": ingest_001_ok,
        "INGEST-002": ingest_002_ok and ingest_graph_ok,
        "INGEST-003": ingest_003_ok,
    }
