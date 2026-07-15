import unittest
from src.delivery_batch_limits import MAX_DELIVERY_BATCH, validate_delivery_batch
class BatchLimitTests(unittest.TestCase):
    def test_accepts_maximum_batch(self): self.assertEqual(len(validate_delivery_batch([{}]*MAX_DELIVERY_BATCH)),MAX_DELIVERY_BATCH)
    def test_rejects_oversized_batch(self):
        with self.assertRaises(ValueError): validate_delivery_batch([{}]*(MAX_DELIVERY_BATCH+1))
if __name__ == "__main__": unittest.main()
