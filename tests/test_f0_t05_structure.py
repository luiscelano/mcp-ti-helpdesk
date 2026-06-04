import unittest
from pathlib import Path


class TestF0T05BaselineStructure(unittest.TestCase):
    def test_required_test_domains_exist_with_test_files(self) -> None:
        root_dir = Path(__file__).resolve().parent
        required_domains = ["SEC", "CLS", "RAG", "GRAPH", "PLAN", "MCP", "INGEST", "INT"]

        missing_domains = []
        domains_without_tests = []

        for domain in required_domains:
            domain_path = root_dir / domain
            if not domain_path.is_dir():
                missing_domains.append(domain)
                continue

            test_files = list(domain_path.glob("test_*.py"))
            if len(test_files) == 0:
                domains_without_tests.append(domain)

        self.assertEqual(missing_domains, [], msg=f"Missing domains: {missing_domains}")
        self.assertEqual(
            domains_without_tests,
            [],
            msg=f"Domains without test files: {domains_without_tests}",
        )


if __name__ == "__main__":
    unittest.main()
