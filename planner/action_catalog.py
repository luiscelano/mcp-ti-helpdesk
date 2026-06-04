from collections import defaultdict
from typing import Dict, List

from ingestion.load_actions import Action, load_actions


class ActionCatalog:
    def __init__(self, actions: List[Action]) -> None:
        if not actions:
            raise ValueError("Action catalog cannot be empty")

        self._actions = list(actions)
        self._by_name: Dict[str, Action] = {}
        self._by_id: Dict[str, Action] = {}
        self._by_effect: Dict[str, List[Action]] = defaultdict(list)

        for action in self._actions:
            if action.nombre in self._by_name:
                raise ValueError(f"Duplicate action name detected: {action.nombre}")
            if action.id in self._by_id:
                raise ValueError(f"Duplicate action id detected: {action.id}")

            self._by_name[action.nombre] = action
            self._by_id[action.id] = action
            for effect in action.efectos:
                self._by_effect[effect].append(action)

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

    def get_action_by_id(self, action_id: str) -> Action:
        if action_id not in self._by_id:
            raise KeyError(f"Action not found: {action_id}")
        return self._by_id[action_id]

    def actions_for_effect(self, effect_name: str) -> List[Action]:
        return list(self._by_effect.get(effect_name, []))

    def validate_domain(self) -> Dict[str, object]:
        action_ids = [action.id for action in self._actions]
        action_names = [action.nombre for action in self._actions]
        effect_index = {
            effect: [action.nombre for action in actions]
            for effect, actions in sorted(self._by_effect.items())
        }

        return {
            "is_valid": True,
            "action_count": len(self._actions),
            "action_ids": action_ids,
            "action_names": action_names,
            "actions_without_preconditions": [
                action.nombre for action in self._actions if not action.precondiciones
            ],
            "effect_index": effect_index,
        }
