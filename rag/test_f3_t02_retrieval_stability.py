import tempfile
import unittest

from rag.search_documents import search_documents


class TestF3T02RetrievalStability(unittest.TestCase):
    def test_retrieval_is_consistent_across_repeated_queries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            runs = [
                search_documents("usuario bloqueado", top_k=2, persist_dir=temp_dir)
                for _ in range(5)
            ]

        ordered_ids = [[item["id"] for item in run["results"]] for run in runs]
        self.assertTrue(all(ids == ordered_ids[0] for ids in ordered_ids[1:]))
        self.assertEqual(ordered_ids[0][0], "POL-001")

    def test_category_filter_limits_results_stably(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = search_documents(
                "usuario bloqueado",
                top_k=3,
                persist_dir=temp_dir,
                category_filters=["acceso"],
            )

        result_ids = [item["id"] for item in result["results"]]
        self.assertEqual(result_ids, ["POL-001"])
        self.assertEqual(result["top_k"], 3)
        self.assertEqual(result["category_filters"], ["acceso"])


if __name__ == "__main__":
    unittest.main()
