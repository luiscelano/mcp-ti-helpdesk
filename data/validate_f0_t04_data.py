import csv
import json
from pathlib import Path
from typing import Dict, List


def validate_data_inputs() -> Dict[str, object]:
    root_dir = Path(__file__).resolve().parent.parent
    data_dir = root_dir / "data"

    files = {
        "archivo1_documentos.json": data_dir / "archivo1_documentos.json",
        "archivo2_grafo.csv": data_dir / "archivo2_grafo.csv",
        "archivo3_acciones.json": data_dir / "archivo3_acciones.json",
    }

    errors: List[str] = []

    for name, path in files.items():
        if not path.exists():
            errors.append(f"Missing required file: {name}")
        elif not path.is_file():
            errors.append(f"Path is not a file: {name}")

    if errors:
        return {"status": "fail", "errors": errors}

    # Validate archivo1_documentos.json structure.
    doc_data = json.loads(files["archivo1_documentos.json"].read_text(encoding="utf-8"))
    if not isinstance(doc_data, list) or len(doc_data) == 0:
        errors.append("archivo1_documentos.json must contain a non-empty list")
    else:
        required_doc_keys = {"id", "titulo", "categoria", "contenido", "palabras_clave"}
        for idx, item in enumerate(doc_data):
            if not isinstance(item, dict):
                errors.append(f"archivo1_documentos.json item {idx} must be an object")
                continue
            missing = required_doc_keys - set(item.keys())
            if missing:
                errors.append(
                    f"archivo1_documentos.json item {idx} missing keys: {sorted(missing)}"
                )

    # Validate archivo2_grafo.csv structure.
    with files["archivo2_grafo.csv"].open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        expected_headers = ["entidad_origen", "relacion", "entidad_destino"]
        if reader.fieldnames != expected_headers:
            errors.append(
                "archivo2_grafo.csv headers must be entidad_origen,relacion,entidad_destino"
            )
        rows = list(reader)
        if len(rows) == 0:
            errors.append("archivo2_grafo.csv must contain at least one relation row")

    # Validate archivo3_acciones.json structure.
    action_data = json.loads(files["archivo3_acciones.json"].read_text(encoding="utf-8"))
    if not isinstance(action_data, list) or len(action_data) == 0:
        errors.append("archivo3_acciones.json must contain a non-empty list")
    else:
        required_action_keys = {"id", "nombre", "costo_minutos", "precondiciones", "efectos"}
        for idx, item in enumerate(action_data):
            if not isinstance(item, dict):
                errors.append(f"archivo3_acciones.json item {idx} must be an object")
                continue
            missing = required_action_keys - set(item.keys())
            if missing:
                errors.append(
                    f"archivo3_acciones.json item {idx} missing keys: {sorted(missing)}"
                )

    return {"status": "pass" if not errors else "fail", "errors": errors}


if __name__ == "__main__":
    result = validate_data_inputs()
    print(json.dumps(result, ensure_ascii=True))
    raise SystemExit(0 if result["status"] == "pass" else 1)
