import unittest

from mcp_server.document_search import search_documents_tool

class TestRAGBaseline(unittest.TestCase):
    def test_rag_regression_access_query_returns_policy(self) -> None:
        response = search_documents_tool(
            query="usuario bloqueado",
            top_k=3,
            persist_dir=".chroma",
            category_filters=["acceso"],
        )

        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["tool"], "search_documents")
        self.assertIn("POL-001", [item["id"] for item in response["results"]])


if __name__ == "__main__":
    unittest.main()
