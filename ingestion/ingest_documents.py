import json
from pathlib import Path
from typing import Dict, List

REQUIRED_DOCUMENT_IDS = ["POL-001", "POL-002", "REG-003", "MAN-004"]
REQUIRED_FIELDS = ["id", "titulo", "categoria", "contenido", "palabras_clave"]


def load_documents(source_path: str | Path = "data/archivo1_documentos.json") -> List[Dict[str, object]]:
    path = Path(source_path)
    raw = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        raise ValueError("Document source must be a JSON list")

    documents: List[Dict[str, object]] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"Document at index {index} must be an object")

        missing = [field for field in REQUIRED_FIELDS if field not in item]
        if missing:
            raise ValueError(
                f"Document at index {index} is missing required fields: {missing}"
            )

        documents.append(
            {
                "id": str(item["id"]),
                "titulo": str(item["titulo"]),
                "categoria": str(item["categoria"]),
                "contenido": str(item["contenido"]),
                "palabras_clave": list(item["palabras_clave"]),
            }
        )

    return documents


def validate_required_documents(documents: List[Dict[str, object]]) -> None:
    available_ids = {str(document["id"]) for document in documents}
    missing_ids = [doc_id for doc_id in REQUIRED_DOCUMENT_IDS if doc_id not in available_ids]
    if missing_ids:
        raise ValueError(f"Missing required documents: {missing_ids}")


def process_documents(source_path: str | Path = "data/archivo1_documentos.json") -> List[Dict[str, object]]:
    documents = load_documents(source_path)
    validate_required_documents(documents)
    return [doc for doc in documents if doc["id"] in REQUIRED_DOCUMENT_IDS]


def build_index_units(source_path: str | Path = "data/archivo1_documentos.json") -> Dict[str, List[object]]:
    documents = process_documents(source_path)

    ids: List[str] = []
    page_contents: List[str] = []
    metadatas: List[Dict[str, object]] = []

    for document in documents:
        document_id = str(document["id"])
        ids.append(document_id)
        page_contents.append(str(document["contenido"]))
        metadatas.append(
            {
                "id": document_id,
                "titulo": str(document["titulo"]),
                "categoria": str(document["categoria"]),
                "palabras_clave": ",".join(str(k) for k in document["palabras_clave"]),
                "unit_type": "full_document",
            }
        )

    return {
        "ids": ids,
        "documents": page_contents,
        "metadatas": metadatas,
    }
