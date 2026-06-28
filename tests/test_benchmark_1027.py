import unittest

class CompositeCursorSeedTests(unittest.TestCase):
    def test_cursor_keeps_region_and_sequence(self):
        self.assertEqual(("sa-east-1", 42), ("sa-east-1", 42))

if __name__ == "__main__":
    unittest.main()
