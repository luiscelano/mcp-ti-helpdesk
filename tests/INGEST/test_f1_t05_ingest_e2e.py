import tempfile
import unittest

from ingestion.validate_ingest_pipeline import run_ingest_end_to_end


class TestF1T05IngestEndToEnd(unittest.TestCase):
    def test_ingest_001_002_003_pass_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_ingest_end_to_end(
                persist_dir=temp_dir,
                collection_name="f1_t05_ingest_e2e",
            )

        self.assertTrue(result["INGEST-001"])
        self.assertTrue(result["INGEST-002"])
        self.assertTrue(result["INGEST-003"])


if __name__ == "__main__":
    unittest.main()
