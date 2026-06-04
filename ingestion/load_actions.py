import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Action:
    id: str
    nombre: str
    costo_minutos: int
    precondiciones: List[str]
    efectos: List[str]


def _validate_action_payload(item: object, index: int) -> Action:
    if not isinstance(item, dict):
        raise ValueError(f"Action at index {index} must be an object")

    required_fields = ["id", "nombre", "costo_minutos", "precondiciones", "efectos"]
    missing = [field for field in required_fields if field not in item]
    if missing:
        raise ValueError(f"Action at index {index} is missing required fields: {missing}")

    action_id = str(item["id"]).strip()
    nombre = str(item["nombre"]).strip()
    costo_minutos = int(item["costo_minutos"])
    precondiciones = item["precondiciones"]
    efectos = item["efectos"]

    if not action_id:
        raise ValueError(f"Action at index {index} has empty id")
    if not nombre:
        raise ValueError(f"Action at index {index} has empty nombre")
    if costo_minutos <= 0:
        raise ValueError(f"Action {action_id} must have costo_minutos > 0")

    if not isinstance(precondiciones, list):
        raise ValueError(f"Action {action_id} precondiciones must be a list")
    if not isinstance(efectos, list):
        raise ValueError(f"Action {action_id} efectos must be a list")
    if not efectos:
        raise ValueError(f"Action {action_id} must define at least one efecto")

    normalized_preconditions = [str(value).strip() for value in precondiciones]
    normalized_effects = [str(value).strip() for value in efectos]

    if any(not value for value in normalized_preconditions):
        raise ValueError(f"Action {action_id} has empty precondicion entries")
    if any(not value for value in normalized_effects):
        raise ValueError(f"Action {action_id} has empty efecto entries")

    return Action(
        id=action_id,
        nombre=nombre,
        costo_minutos=costo_minutos,
        precondiciones=normalized_preconditions,
        efectos=normalized_effects,
    )


def load_actions(source_path: str | Path = "data/archivo3_acciones.json") -> List[Action]:
    path = Path(source_path)
    payload = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(payload, list) or not payload:
        raise ValueError("Action source must be a non-empty JSON list")

    actions: List[Action] = []
    seen_ids = set()
    for index, item in enumerate(payload):
        action = _validate_action_payload(item, index)
        if action.id in seen_ids:
            raise ValueError(f"Duplicate action id detected: {action.id}")
        seen_ids.add(action.id)
        actions.append(action)

    return actions
