import unittest

from ingestion.load_actions import load_actions
from planner.action_catalog import ActionCatalog


class TestF1T04LoadActions(unittest.TestCase):
    def test_actions_are_available_for_planner_with_valid_rules(self) -> None:
        actions = load_actions("data/archivo3_acciones.json")
        self.assertGreaterEqual(len(actions), 6)

        for action in actions:
            self.assertGreater(action.costo_minutos, 0)
            self.assertIsInstance(action.precondiciones, list)
            self.assertIsInstance(action.efectos, list)
            self.assertGreater(len(action.efectos), 0)
            self.assertTrue(all(value.strip() for value in action.precondiciones))
            self.assertTrue(all(value.strip() for value in action.efectos))

        catalog = ActionCatalog.from_json("data/archivo3_acciones.json")
        selected = catalog.get_action("enviar_solicitud_IAM")
        self.assertIn("identidad_verificada", selected.precondiciones)
        self.assertIn("solicitud_enviada", selected.efectos)


if __name__ == "__main__":
    unittest.main()
