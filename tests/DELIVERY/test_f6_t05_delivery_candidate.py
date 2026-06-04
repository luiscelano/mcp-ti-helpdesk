import unittest
from pathlib import Path


class TestF6T05DeliveryCandidate(unittest.TestCase):
    def setUp(self) -> None:
        root_dir = Path(__file__).resolve().parents[2]
        self.root_dir = root_dir
        self.delivery_candidate = (root_dir / "docs" / "DELIVERY_CANDIDATE.md").read_text(encoding="utf-8")
        self.f6_t05_script = (root_dir / "tests" / "f6_t05_acceptance_test.sh").read_text(encoding="utf-8")

    def test_delivery_candidate_declares_executable_and_demo_and_traceability(self) -> None:
        self.assertIn("Entrega ejecutable", self.delivery_candidate)
        self.assertIn("Entrega demostrable", self.delivery_candidate)
        self.assertIn("Entrega trazable", self.delivery_candidate)

    def test_traceability_matrix_covers_all_required_domains(self) -> None:
        required_domains = ["SEC", "CLS", "RAG", "GRAPH", "PLAN", "MCP", "INGEST", "INT"]
        for domain in required_domains:
            self.assertIn(domain, self.delivery_candidate)

    def test_referenced_test_files_exist(self) -> None:
        required_files = [
            "tests/SEC/test_sec_baseline.py",
            "tests/CLS/test_cls_baseline.py",
            "tests/RAG/test_rag_baseline.py",
            "tests/GRAPH/test_graph_baseline.py",
            "tests/PLAN/test_plan_baseline.py",
            "tests/MCP/test_mcp_baseline.py",
            "tests/INGEST/test_ingest_baseline.py",
            "tests/INT/test_int_baseline.py",
            "tests/f6_t01_acceptance_test.sh",
            "tests/f6_t02_acceptance_test.sh",
            "tests/f6_t03_acceptance_test.sh",
            "tests/f6_t04_acceptance_test.sh",
        ]
        for rel_path in required_files:
            self.assertTrue((self.root_dir / rel_path).exists(), msg=f"Missing file: {rel_path}")

    def test_f6_t05_acceptance_runs_final_phase_validations(self) -> None:
        self.assertIn("./tests/f6_t01_acceptance_test.sh", self.f6_t05_script)
        self.assertIn("./tests/f6_t02_acceptance_test.sh", self.f6_t05_script)
        self.assertIn("./tests/f6_t03_acceptance_test.sh", self.f6_t05_script)
        self.assertIn("./tests/f6_t04_acceptance_test.sh", self.f6_t05_script)
        self.assertIn("tests.DELIVERY.test_f6_t05_delivery_candidate", self.f6_t05_script)


if __name__ == "__main__":
    unittest.main()
