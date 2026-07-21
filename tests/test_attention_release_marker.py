import unittest

from src.attention_release_marker import parse_release_marker


class ReleaseMarkerTests(unittest.TestCase):
    def test_parses_explicit_channel(self):
        self.assertEqual(parse_release_marker("ga:4.7"), ("ga", "4.7"))

    def test_rejects_omitted_channel(self):
        with self.assertRaises(ValueError):
            parse_release_marker("4.7")


if __name__ == "__main__":
    unittest.main()
