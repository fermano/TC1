import unittest

from src.coverage_seed_webhook_time import webhook_timestamp_is_fresh


class WebhookTimestampTests(unittest.TestCase):
    def test_recent_timestamp_is_fresh(self):
        self.assertTrue(webhook_timestamp_is_fresh("970", now=1000))

    def test_stale_timestamp_is_rejected(self):
        self.assertFalse(webhook_timestamp_is_fresh("600", now=1000))

    def test_future_timestamp_is_rejected(self):
        self.assertFalse(webhook_timestamp_is_fresh("1030", now=1000))

    def test_malformed_timestamp_is_rejected(self):
        self.assertFalse(webhook_timestamp_is_fresh("not-a-time", now=1000))


if __name__ == "__main__":
    unittest.main()
