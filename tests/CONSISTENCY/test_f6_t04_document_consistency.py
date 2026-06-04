import unittest
from pathlib import Path


class TestF6T04DocumentConsistency(unittest.TestCase):
    def setUp(self) -> None:
        root_dir = Path(__file__).resolve().parents[2]
        docs_dir = root_dir / "docs"
        self.architecture = (docs_dir / "architecture.md").read_text(encoding="utf-8")
        self.specifications = (docs_dir / "specifications.md").read_text(encoding="utf-8")
        self.project_readiness = (docs_dir / "PROJECT_READINESS.md").read_text(encoding="utf-8")
        self.implementation_plan = (docs_dir / "IMPLEMENTATION_PLAN.md").read_text(encoding="utf-8")

    def test_ingestion_contract_is_consistent_between_architecture_and_plan(self) -> None:
        self.assertIn("data/archivo1_documentos.json", self.architecture)
        self.assertIn("No se realizará fragmentación (chunking) documental.", self.architecture)
        self.assertIn("data/archivo1_documentos.json", self.implementation_plan)

    def test_architecture_no_longer_contains_critical_pdf_chunking_contradiction(self) -> None:
        self.assertNotIn(
            "Los documentos PDF proporcionados por el proyecto serán procesados para:",
            self.architecture,
        )
        self.assertNotIn("Dividir contenido en fragmentos.", self.architecture)

    def test_security_flow_consistency_across_specs_and_plan(self) -> None:
        self.assertIn("## RULE-002", self.specifications)
        self.assertIn("## RULE-003", self.specifications)
        self.assertIn(
            "Regla global: ninguna solicitud bloqueada avanza a RAG/GraphRAG.",
            self.implementation_plan,
        )

    def test_f6_t04_consistency_result_is_recorded(self) -> None:
        self.assertIn("## Validacion Final de Consistencia Documental (F6-T04)", self.project_readiness)
        self.assertIn("Sin contradicciones criticas", self.project_readiness)
        self.assertIn("## Resultado F6-T04 - Consistencia Documental", self.implementation_plan)
        self.assertIn("No se identifican contradicciones criticas activas", self.implementation_plan)


if __name__ == "__main__":
    unittest.main()
