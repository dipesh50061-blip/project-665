import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from main import backoff_delay


class TestBackoffDelay(unittest.TestCase):
    def test_grows_exponentially_and_caps(self):
        self.assertEqual(backoff_delay(0), 1.0)
        self.assertEqual(backoff_delay(3), 8.0)
        self.assertEqual(backoff_delay(10, maximum_seconds=30), 30)

    def test_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            backoff_delay(-1)


if __name__ == "__main__":
    unittest.main()
