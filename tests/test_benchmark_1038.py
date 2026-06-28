import unittest

class HybridClockSeedTests(unittest.TestCase):
    def test_clock_regression_keeps_total_order(self):
        emitted = [1002, 998]
        self.assertEqual(emitted, sorted(emitted), "clock regression reverses audit order")

if __name__ == "__main__":
    unittest.main()
