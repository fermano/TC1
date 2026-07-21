import unittest

from src.coverage_seed_outcomes import categorize_delivery_outcome


class DeliveryOutcomeTests(unittest.TestCase):
    def test_all_declared_outcomes(self):
        cases = {
            "sent": "success",
            "delivered": "success",
            "retry": "retry",
            "rate_limited": "retry",
            "rejected": "dropped",
            "expired": "dropped",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(categorize_delivery_outcome(value), expected)

    def test_normalizes_case_and_whitespace(self):
        self.assertEqual(categorize_delivery_outcome("  SENT "), "success")

    def test_unknown_empty_and_none(self):
        for value in ("other", "", None):
            with self.subTest(value=value):
                self.assertEqual(categorize_delivery_outcome(value), "unknown")


if __name__ == "__main__":
    unittest.main()
