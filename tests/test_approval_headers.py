import unittest

from src.approval_headers import parse_approval_header


class ApprovalHeaderTests(unittest.TestCase):
    def test_valid_header_returns_owner(self):
        self.assertEqual(
            parse_approval_header("approved-by: release-operations"),
            "release-operations",
        )

    def test_empty_owner_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_approval_header("approved-by:   ")

    def test_unknown_header_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_approval_header("reviewed-by: platform")


if __name__ == "__main__":
    unittest.main()
