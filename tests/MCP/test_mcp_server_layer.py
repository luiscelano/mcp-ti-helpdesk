import unittest
from unittest.mock import patch

import mcp_server.server as server


class TestMCPLayerFastMCP(unittest.TestCase):
    @patch("mcp_server.server.resolve_incident_tool")
    def test_resolve_incident_tool_wrapper(self, mock_resolve_incident_tool) -> None:
        mock_resolve_incident_tool.return_value = {"status": "allowed"}

        response = server.resolve_incident("Mi usuario esta bloqueado")

        self.assertEqual(response, {"status": "allowed"})
        mock_resolve_incident_tool.assert_called_once_with("Mi usuario esta bloqueado")

    @patch("mcp_server.server.search_documents_tool")
    def test_search_documents_tool_wrapper(self, mock_search_documents_tool) -> None:
        mock_search_documents_tool.return_value = {"tool": "search_documents", "status": "ok"}

        response = server.search_documents(
            query="usuario bloqueado",
            top_k=5,
            persist_dir=".chroma",
            category_filters=["acceso"],
        )

        self.assertEqual(response["tool"], "search_documents")
        self.assertEqual(response["status"], "ok")
        mock_search_documents_tool.assert_called_once_with(
            query="usuario bloqueado",
            top_k=5,
            persist_dir=".chroma",
            category_filters=["acceso"],
        )

    @patch("mcp_server.server.search_graph_tool")
    def test_search_graph_tool_wrapper(self, mock_search_graph_tool) -> None:
        mock_search_graph_tool.return_value = {"tool": "search_graph", "status": "ok"}

        response = server.search_graph(node_name="AccesoBloqueado", depth=2)

        self.assertEqual(response["tool"], "search_graph")
        self.assertEqual(response["status"], "ok")
        mock_search_graph_tool.assert_called_once_with(node_name="AccesoBloqueado", depth=2)

    @patch("mcp_server.server.plan_resolution_tool")
    def test_plan_resolution_tool_wrapper(self, mock_plan_resolution_tool) -> None:
        mock_plan_resolution_tool.return_value = {"tool": "plan_resolution", "status": "ok"}

        response = server.plan_resolution(
            goal_fact="usuario_desbloqueado",
            initial_facts=["identidad_verificada"],
            plan=None,
            source_path="data/archivo3_acciones.json",
        )

        self.assertEqual(response["tool"], "plan_resolution")
        self.assertEqual(response["status"], "ok")
        mock_plan_resolution_tool.assert_called_once_with(
            goal_fact="usuario_desbloqueado",
            initial_facts=["identidad_verificada"],
            plan=None,
            source_path="data/archivo3_acciones.json",
        )

    def test_run_stdio_server_uses_stdio_transport(self) -> None:
        with patch.object(server.mcp, "run") as mock_run:
            server.run_stdio_server()

        mock_run.assert_called_once_with(transport="stdio")


if __name__ == "__main__":
    unittest.main()
