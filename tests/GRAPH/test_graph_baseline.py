import unittest

from mcp_server.graph_search import search_graph_tool

class TestGRAPHBaseline(unittest.TestCase):
    def test_graph_regression_access_blocked_relations(self) -> None:
        response = search_graph_tool(node_name="AccesoBloqueado", depth=2)

        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["tool"], "search_graph")
        self.assertIn("AccesoBloqueado -> DesbloqueoIAM", response["results"])


if __name__ == "__main__":
    unittest.main()
