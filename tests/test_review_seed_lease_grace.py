import unittest

from src.review_seed_lease_grace import (
    DEFAULT_LEASE_GRACE_SECONDS,
    effective_lease_grace,
)


class LeaseGraceTests(unittest.TestCase):
    def test_missing_value_uses_default(self):
        self.assertEqual(effective_lease_grace(None), DEFAULT_LEASE_GRACE_SECONDS)

    def test_positive_override_is_preserved(self):
        self.assertEqual(effective_lease_grace(12), 12)


if __name__ == "__main__":
    unittest.main()
