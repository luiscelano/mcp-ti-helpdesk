from pathlib import Path
from typing import Dict, List, Optional

import chromadb

from ingestion.ingest_documents import build_index_units


def index_documents_no_chunking(
    source_path: str | Path = "data/archivo1_documentos.json",
    persist_dir: str | Path = ".chroma",
    collection_name: str = "ti_helpdesk_documents",
    embedding_function: Optional[object] = None,
) -> Dict[str, object]:
    payload = build_index_units(source_path)

    client = chromadb.PersistentClient(path=str(persist_dir))
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function,
        metadata={"indexing_strategy": "no_chunking"},
    )

    collection.upsert(
        ids=payload["ids"],
        documents=payload["documents"],
        metadatas=payload["metadatas"],
    )

    count = collection.count()
    return {
        "collection_name": collection_name,
        "indexed_count": count,
        "indexed_ids": list(payload["ids"]),
    }
