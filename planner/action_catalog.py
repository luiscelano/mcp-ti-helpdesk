from typing import Dict, List

from ingestion.load_actions import Action, load_actions


class ActionCatalog:
    def __init__(self, actions: List[Action]) -> None:
        self._actions = actions
        self._by_name: Dict[str, Action] = {action.nombre: action for action in actions}

    @classmethod
    def from_json(cls, source_path: str = "data/archivo3_acciones.json") -> "ActionCatalog":
        actions = load_actions(source_path)
        return cls(actions)

    def all_actions(self) -> List[Action]:
        return list(self._actions)

    def get_action(self, action_name: str) -> Action:
        if action_name not in self._by_name:
            raise KeyError(f"Action not found: {action_name}")
        return self._by_name[action_name]
