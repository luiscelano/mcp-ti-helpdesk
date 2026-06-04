import tempfile
import unittest

from mcp_server.document_search import search_documents_tool
from mcp_server.graph_search import search_graph_tool


class TestF3T04ToolsContract(unittest.TestCase):
    def test_search_documents_tool_has_stable_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            response = search_documents_tool(
                query="usuario bloqueado",
                top_k=2,
                persist_dir=temp_dir,
                category_filters=["acceso"],
            )

        self.assertEqual(response["tool"], "search_documents")
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["query"], "usuario bloqueado")
        self.assertEqual(response["parameters"]["top_k"], 2)
        self.assertEqual(response["parameters"]["category_filters"], ["acceso"])
        self.assertGreaterEqual(response["result_count"], 1)
        self.assertIsInstance(response["results"], list)
        self.assertIn("POL-001", [item["id"] for item in response["results"]])

    def test_search_graph_tool_has_stable_contract(self) -> None:
        response = search_graph_tool(node_name="AccesoBloqueado", depth=2)

        self.assertEqual(response["tool"], "search_graph")
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["query"], "AccesoBloqueado")
        self.assertEqual(response["parameters"]["depth"], 2)
        self.assertGreaterEqual(response["result_count"], 3)
        self.assertIn("AccesoBloqueado -> DesbloqueoIAM", response["results"])
        self.assertIn("DesbloqueoIAM -> VerificacionIdentidad", response["results"])
        self.assertIn("DesbloqueoIAM -> OficialCumplimiento", response["results"])


if __name__ == "__main__":
    unittest.main()
