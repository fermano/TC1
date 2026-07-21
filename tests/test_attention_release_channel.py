import unittest

from src.attention_release_channel import normalize_release_channel


class ReleaseChannelTests(unittest.TestCase):
    def test_stable_maps_to_ga(self):
        self.assertEqual(normalize_release_channel(" Stable "), "ga")


if __name__ == "__main__":
    unittest.main()
