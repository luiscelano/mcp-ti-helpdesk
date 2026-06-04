import unittest

from ingestion.load_actions import Action
from planner.action_catalog import ActionCatalog
from planner.backward_chaining import (
    build_backward_chaining_plan,
    build_backward_chaining_plan_from_catalog,
    plan_is_valid,
    validate_plan_execution,
)


class TestF4T02BackwardChaining(unittest.TestCase):
    def test_backward_chaining_generates_unlock_plan(self) -> None:
        result = build_backward_chaining_plan("usuario_desbloqueado")

        self.assertTrue(result["is_valid"])
        self.assertEqual(result["goal"], "usuario_desbloqueado")
        self.assertEqual(
            result["plan"],
            ["verificar_identidad", "enviar_solicitud_IAM", "esperar_confirmacion_IAM"],
        )
        self.assertEqual(result["total_cost"], 10)
        self.assertIn("usuario_desbloqueado", result["final_facts"])
        self.assertTrue(plan_is_valid(result["plan"]))

    def test_backward_chaining_reuses_known_facts(self) -> None:
        result = build_backward_chaining_plan(
            "usuario_desbloqueado",
            initial_facts=["identidad_verificada"],
        )

        self.assertEqual(
            result["plan"],
            ["enviar_solicitud_IAM", "esperar_confirmacion_IAM"],
        )
        self.assertEqual(result["total_cost"], 7)
        self.assertTrue(plan_is_valid(result["plan"], ["identidad_verificada"]))

    def test_invalid_action_is_blocked_when_preconditions_are_missing(self) -> None:
        result = validate_plan_execution(["enviar_solicitud_IAM"], initial_facts=[])

        self.assertFalse(result["is_valid"])
        self.assertEqual(result["blocked_action"], "enviar_solicitud_IAM")
        self.assertEqual(result["missing_preconditions"], ["identidad_verificada"])
        self.assertEqual(result["executed_actions"], [])
        self.assertEqual(result["known_facts"], [])

    def test_valid_plan_execution_advances_through_all_actions(self) -> None:
        result = validate_plan_execution(
            ["verificar_identidad", "enviar_solicitud_IAM"],
            initial_facts=[],
        )

        self.assertTrue(result["is_valid"])
        self.assertIsNone(result["blocked_action"])
        self.assertEqual(
            result["executed_actions"],
            ["verificar_identidad", "enviar_solicitud_IAM"],
        )
        self.assertIn("solicitud_enviada", result["known_facts"])

    def test_selects_lowest_cost_plan_when_alternatives_exist(self) -> None:
        catalog = ActionCatalog(
            [
                Action(
                    id="ALT-01",
                    nombre="preparar_rapido",
                    costo_minutos=1,
                    precondiciones=[],
                    efectos=["entorno_preparado"],
                ),
                Action(
                    id="ALT-02",
                    nombre="preparar_lento",
                    costo_minutos=5,
                    precondiciones=[],
                    efectos=["entorno_preparado"],
                ),
                Action(
                    id="ALT-03",
                    nombre="finalizar_tarea",
                    costo_minutos=2,
                    precondiciones=["entorno_preparado"],
                    efectos=["tarea_completada"],
                ),
            ]
        )

        result = build_backward_chaining_plan_from_catalog("tarea_completada", catalog)

        self.assertEqual(result["plan"], ["preparar_rapido", "finalizar_tarea"])
        self.assertEqual(result["total_cost"], 3)
        self.assertTrue(plan_is_valid(result["plan"], catalog=catalog))


if __name__ == "__main__":
    unittest.main()
