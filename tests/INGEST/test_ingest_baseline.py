import tempfile
import unittest

from ingestion.validate_ingest_pipeline import run_ingest_end_to_end

class TestINGESTBaseline(unittest.TestCase):
    def test_ingest_regression_pipeline_flags_are_true(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_ingest_end_to_end(
                persist_dir=temp_dir,
                collection_name="f6_t01_ingest_regression",
            )

        self.assertTrue(result["INGEST-001"])
        self.assertTrue(result["INGEST-002"])
        self.assertTrue(result["INGEST-003"])


if __name__ == "__main__":
    unittest.main()
