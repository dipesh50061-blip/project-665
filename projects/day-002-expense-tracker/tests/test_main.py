import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from main import monthly_total


class TestDay002(unittest.TestCase):
    def test_happy_path(self):
        self.assertEqual(monthly_total([{"date": "2026-09-01", "amount": 12.5}, {"date": "2026-08-31", "amount": 99}], "2026-09"), 12.5)


if __name__ == "__main__":
    unittest.main()
