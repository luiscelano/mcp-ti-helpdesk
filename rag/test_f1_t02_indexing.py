import tempfile
import unittest

from rag.chroma_indexer import index_documents_no_chunking


class FakeEmbeddingFunction:
    def __call__(self, input):
        return [[0.0, 0.0, 0.0] for _ in input]

    def name(self) -> str:
        return "fake"

    def is_legacy(self) -> bool:
        return False


class TestF1T02Indexing(unittest.TestCase):
    def test_creates_collection_and_indexes_four_full_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = index_documents_no_chunking(
                source_path="data/archivo1_documentos.json",
                persist_dir=temp_dir,
                collection_name="f1_t02_test_collection",
                embedding_function=FakeEmbeddingFunction(),
            )

        self.assertEqual(result["collection_name"], "f1_t02_test_collection")
        self.assertEqual(result["indexed_count"], 4)
        self.assertEqual(
            set(result["indexed_ids"]),
            {"POL-001", "POL-002", "REG-003", "MAN-004"},
        )


if __name__ == "__main__":
    unittest.main()
