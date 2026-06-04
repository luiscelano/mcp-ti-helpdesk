import unittest
from pathlib import Path


class TestF6T03RiskReadiness(unittest.TestCase):
    def setUp(self) -> None:
        root_dir = Path(__file__).resolve().parents[2]
        self.project_readiness = (root_dir / "docs" / "PROJECT_READINESS.md").read_text(encoding="utf-8")
        self.implementation_plan = (root_dir / "docs" / "IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")

    def test_project_readiness_includes_prioritized_open_risks(self) -> None:
        self.assertIn("## Riesgos Residuales Abiertos Priorizados", self.project_readiness)
        self.assertIn("Prioridad", self.project_readiness)
        self.assertIn("Riesgo residual abierto", self.project_readiness)
        self.assertIn("P0", self.project_readiness)
        self.assertIn("P1", self.project_readiness)
        self.assertIn("P2", self.project_readiness)

    def test_project_readiness_defines_mitigation_and_post_delivery_plan(self) -> None:
        self.assertIn("Mitigacion inmediata", self.project_readiness)
        self.assertIn("Plan post-entrega", self.project_readiness)
        self.assertIn("Criterio de seguimiento", self.project_readiness)

    def test_implementation_plan_includes_post_delivery_risk_backlog(self) -> None:
        self.assertIn("## Plan Post-Entrega de Riesgos Residuales", self.implementation_plan)
        self.assertIn("Semana 1 post-entrega", self.implementation_plan)
        self.assertIn("Semana 2 post-entrega", self.implementation_plan)
        self.assertIn("Semana 3 post-entrega", self.implementation_plan)
        self.assertIn("Criterio de cierre de riesgos", self.implementation_plan)


if __name__ == "__main__":
    unittest.main()
