import unittest

from ingestion.load_graph import load_graph_from_csv, run_graph_validation_queries


class TestF1T03LoadGraph(unittest.TestCase):
    def test_loads_graph_and_passes_required_graph_queries(self) -> None:
        load_result = load_graph_from_csv("data/archivo2_grafo.csv")
        self.assertGreaterEqual(load_result["relationships_loaded"], 9)

        validation = run_graph_validation_queries()
        self.assertTrue(validation["GRAPH-001"])
        self.assertTrue(validation["GRAPH-002"])
        self.assertTrue(validation["GRAPH-003"])


if __name__ == "__main__":
    unittest.main()
