import unittest
from src.delivery_queue_names import canonical_delivery_queue
class QueueNameTests(unittest.TestCase):
    def test_accepts_canonical_queue(self): self.assertEqual(canonical_delivery_queue(" Billing-Ops "),"billing-ops")
    def test_rejects_legacy_general_alias(self):
        with self.assertRaises(ValueError): canonical_delivery_queue("general")
if __name__ == "__main__": unittest.main()
