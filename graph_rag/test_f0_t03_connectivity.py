import unittest

from graph_rag.validate_neo4j_connection import run_connectivity_check


class TestF0T03Connectivity(unittest.TestCase):
    def test_neo4j_aura_connection_and_minimal_query(self) -> None:
        result = run_connectivity_check()
        self.assertEqual(result["status"], "pass", msg=result.get("error"))
        self.assertTrue(result["authenticated"], msg=result.get("error"))
        self.assertTrue(result["query_ok"], msg=result.get("error"))


if __name__ == "__main__":
    unittest.main()
