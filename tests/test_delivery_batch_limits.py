import unittest
from src.delivery_batch_limits import (
    MAX_DELIVERY_BATCH,
    PARTNER_RETRY_BATCH,
    validate_delivery_batch,
)


class BatchLimitTests(unittest.TestCase):
    def test_accepts_maximum_batch(self):
        self.assertEqual(
            len(validate_delivery_batch([{}] * MAX_DELIVERY_BATCH)),
            MAX_DELIVERY_BATCH,
        )

    def test_rejects_oversized_batch(self):
        with self.assertRaises(ValueError):
            validate_delivery_batch([{}] * (MAX_DELIVERY_BATCH + 1))

    def test_partner_retry_uses_forty_record_limit(self):
        self.assertEqual(
            len(validate_delivery_batch([{}] * PARTNER_RETRY_BATCH, queue="partner-retry")),
            PARTNER_RETRY_BATCH,
        )
        with self.assertRaises(ValueError):
            validate_delivery_batch([{}] * (PARTNER_RETRY_BATCH + 1), queue="partner-retry")

    def test_partner_import_keeps_general_limit(self):
        self.assertEqual(
            len(validate_delivery_batch([{}] * MAX_DELIVERY_BATCH, queue="partner-import")),
            MAX_DELIVERY_BATCH,
        )


if __name__ == "__main__":
    unittest.main()
