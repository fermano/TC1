import unittest

from src.seed_audit_composite_cursor import (
    encode_composite_cursor,
    page_after_composite_cursor,
)


class CompositeCursorTests(unittest.TestCase):
    def test_resume_inside_same_timestamp_group(self):
        records = [
            {"id": "evt-a", "occurred_at": 100},
            {"id": "evt-b", "occurred_at": 100},
        ]
        cursor = encode_composite_cursor(records[0])
        self.assertEqual(
            [item["id"] for item in page_after_composite_cursor(records, cursor, 1)],
            ["evt-b"],
        )

    def test_accepts_legacy_decimal_cursor(self):
        records = [
            {"id": "evt-a", "occurred_at": 100},
            {"id": "evt-b", "occurred_at": 101},
        ]
        self.assertEqual(
            [item["id"] for item in page_after_composite_cursor(records, "100")],
            ["evt-b"],
        )


if __name__ == "__main__":
    unittest.main()
