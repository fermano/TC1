import unittest

from src.seed_audit_cursor import encode_audit_cursor, page_after_cursor


class AuditCursorTests(unittest.TestCase):
    def test_first_page_is_stably_ordered(self):
        records = [
            {"id": "evt-b", "occurred_at": 102},
            {"id": "evt-a", "occurred_at": 101},
        ]
        self.assertEqual(
            [item["id"] for item in page_after_cursor(records, limit=2)],
            ["evt-a", "evt-b"],
        )

    def test_resume_after_prior_timestamp(self):
        records = [
            {"id": "evt-a", "occurred_at": 101},
            {"id": "evt-b", "occurred_at": 102},
        ]
        cursor = encode_audit_cursor(records[0])
        self.assertEqual(
            [item["id"] for item in page_after_cursor(records, cursor=cursor)],
            ["evt-b"],
        )


if __name__ == "__main__":
    unittest.main()
