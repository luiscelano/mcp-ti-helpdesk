import unittest

from mcp_server.document_search import search_documents_tool
from mcp_server.graph_search import search_graph_tool
from mcp_server.resolve_incident import resolve_incident_tool


class TestF3T05CombinedRetrieval(unittest.TestCase):
    def test_int_001_combines_rag_and_graphrag_signals(self) -> None:
        rag_response = search_documents_tool(
            query="No puedo acceder a mi usuario de préstamos.",
            top_k=3,
            persist_dir=".chroma",
            category_filters=["acceso"],
        )
        graph_response = search_graph_tool(node_name="AccesoBloqueado", depth=2)

        self.assertEqual(rag_response["tool"], "search_documents")
        self.assertEqual(rag_response["status"], "ok")
        self.assertEqual(rag_response["parameters"]["top_k"], 3)
        self.assertEqual(rag_response["parameters"]["category_filters"], ["acceso"])
        self.assertIn("POL-001", [item["id"] for item in rag_response["results"]])

        self.assertEqual(graph_response["tool"], "search_graph")
        self.assertEqual(graph_response["status"], "ok")
        self.assertEqual(graph_response["parameters"]["depth"], 2)
        self.assertIn("AccesoBloqueado -> DesbloqueoIAM", graph_response["results"])
        self.assertIn("DesbloqueoIAM -> VerificacionIdentidad", graph_response["results"])
        self.assertIn("DesbloqueoIAM -> OficialCumplimiento", graph_response["results"])

    def test_int_001_expected_combined_summary_values(self) -> None:
        rag_response = search_documents_tool(
            query="No puedo acceder a mi usuario de préstamos.",
            top_k=3,
            persist_dir=".chroma",
            category_filters=["acceso"],
        )
        graph_response = search_graph_tool(node_name="AccesoBloqueado", depth=2)

        combined_summary = {
            "classification": {"category": "acceso"},
            "rag_results": [item["id"] for item in rag_response["results"]],
            "graph_results": graph_response["results"],
        }

        self.assertEqual(combined_summary["classification"]["category"], "acceso")
        self.assertIn("POL-001", combined_summary["rag_results"])
        self.assertIn("AccesoBloqueado -> DesbloqueoIAM", combined_summary["graph_results"])


class TestF5T05Int001EndToEnd(unittest.TestCase):
    def test_int_001_resolve_incident_returns_expected_structure_and_content(self) -> None:
        response = resolve_incident_tool("No puedo acceder a mi usuario de préstamos.")

        self.assertEqual(response["status"], "allowed")
        self.assertEqual(response["classification"].get("category"), "acceso")
        self.assertIn("POL-001", response["rag_results"])
        self.assertIn("AccesoBloqueado -> DesbloqueoIAM", response["graph_results"])
        self.assertEqual(
            response["resolution_plan"],
            ["verificar_identidad", "enviar_solicitud_IAM", "esperar_confirmacion_IAM"],
        )
        self.assertIsInstance(response["final_response"], str)
        self.assertNotEqual(response["final_response"].strip(), "")


if __name__ == "__main__":
    unittest.main()
