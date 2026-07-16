import unittest

from src.review_seed_delivery_metrics import delivery_attempt_labels


class DeliveryAttemptLabelTests(unittest.TestCase):
    def test_returns_only_bounded_labels(self):
        record = {
            "queue": "priority",
            "outcome": "retried",
            "delivery_id": "delivery-928173",
        }
        self.assertEqual(
            delivery_attempt_labels(record),
            {"queue": "priority", "outcome": "retried"},
        )

    def test_does_not_mutate_input(self):
        record = {"queue": "bulk", "outcome": "sent", "delivery_id": "d-1"}
        before = dict(record)
        delivery_attempt_labels(record)
        self.assertEqual(record, before)


if __name__ == "__main__":
    unittest.main()
