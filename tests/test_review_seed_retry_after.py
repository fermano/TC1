import unittest

from src.review_seed_retry_after import parse_retry_after


class RetryAfterTests(unittest.TestCase):
    def test_numeric_delay(self):
        self.assertEqual(parse_retry_after("120"), 120)

    def test_http_date_delay(self):
        self.assertEqual(
            parse_retry_after("Thu, 16 Jul 2026 20:00:10 GMT", now_epoch=1784232000),
            10,
        )


if __name__ == "__main__":
    unittest.main()
