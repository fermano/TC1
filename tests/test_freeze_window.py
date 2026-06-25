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


if __name__ == "__main__":
    unittest.main()
