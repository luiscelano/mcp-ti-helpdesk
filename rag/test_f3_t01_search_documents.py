import tempfile
import unittest

from rag.search_documents import search_documents


class TestF3T01SearchDocuments(unittest.TestCase):
    def test_rag_001_recovers_pol_001(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = search_documents("usuario bloqueado", persist_dir=temp_dir)

        top_ids = [item["id"] for item in result["results"]]
        self.assertIn("POL-001", top_ids)

    def test_rag_002_recovers_pol_002(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = search_documents("impresora no imprime", persist_dir=temp_dir)

        top_ids = [item["id"] for item in result["results"]]
        self.assertIn("POL-002", top_ids)

    def test_rag_003_recovers_man_004(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = search_documents(
                "sistema de préstamos no funciona", persist_dir=temp_dir
            )

        top_ids = [item["id"] for item in result["results"]]
        self.assertIn("MAN-004", top_ids)


if __name__ == "__main__":
    unittest.main()