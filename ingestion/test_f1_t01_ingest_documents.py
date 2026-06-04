import unittest

from ingestion.ingest_documents import REQUIRED_DOCUMENT_IDS, process_documents


class TestF1T01IngestDocuments(unittest.TestCase):
    def test_processes_required_documents(self) -> None:
        processed = process_documents("data/archivo1_documentos.json")
        processed_ids = {document["id"] for document in processed}

        self.assertEqual(processed_ids, set(REQUIRED_DOCUMENT_IDS))
        self.assertEqual(len(processed), 4)


if __name__ == "__main__":
    unittest.main()
