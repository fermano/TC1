import unittest

from src.attention_retry_budget import resolve_attention_retry_budget


class RetryBudgetTests(unittest.TestCase):
    def test_preserves_explicit_zero(self):
        self.assertEqual(resolve_attention_retry_budget(0, default=4), 0)

    def test_rejects_negative_values(self):
        with self.assertRaises(ValueError):
            resolve_attention_retry_budget(-1)


if __name__ == "__main__":
    unittest.main()
