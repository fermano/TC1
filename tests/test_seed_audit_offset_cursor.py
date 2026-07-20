import unittest

from src.seed_audit_offset_cursor import page_from_offset


class OffsetCursorTests(unittest.TestCase):
    def test_static_pages_do_not_repeat_or_omit(self):
        records = [
            {"id": "evt-a", "occurred_at": 100},
            {"id": "evt-b", "occurred_at": 100},
            {"id": "evt-c", "occurred_at": 101},
        ]
        first, cursor = page_from_offset(records, limit=1)
        second, _ = page_from_offset(records, offset=int(cursor), limit=2)
        self.assertEqual([item["id"] for item in first + second], ["evt-a", "evt-b", "evt-c"])


if __name__ == "__main__":
    unittest.main()
