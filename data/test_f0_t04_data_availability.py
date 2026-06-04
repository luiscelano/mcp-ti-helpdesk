import unittest

from data.validate_f0_t04_data import validate_data_inputs


class TestF0T04DataAvailability(unittest.TestCase):
    def test_data_files_exist_and_have_expected_structure(self) -> None:
        result = validate_data_inputs()
        self.assertEqual(result["status"], "pass", msg="; ".join(result["errors"]))


if __name__ == "__main__":
    unittest.main()
