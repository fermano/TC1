import unittest
from datetime import datetime, timezone

from src.freeze_window import is_in_freeze_window


class FreezeWindowTests(unittest.TestCase):
    def test_region_local_hour_is_used(self):
        instant = datetime(2026, 6, 25, 14, 0, tzinfo=timezone.utc)

        self.assertTrue(
            is_in_freeze_window(instant, "America/New_York", 9, 12)
        )
        self.assertFalse(
            is_in_freeze_window(instant, "America/Los_Angeles", 9, 12)
        )

    def test_dst_transition_uses_region_offset_before_and_after_change(self):
        before_transition = datetime(2026, 3, 8, 6, 30, tzinfo=timezone.utc)
        after_transition = datetime(2026, 3, 8, 7, 30, tzinfo=timezone.utc)

        self.assertTrue(
            is_in_freeze_window(
                before_transition,
                "America/New_York",
                1,
                2,
            )
        )
        self.assertFalse(
            is_in_freeze_window(
                after_transition,
                "America/New_York",
                1,
                2,
            )
        )


if __name__ == "__main__":
    unittest.main()
