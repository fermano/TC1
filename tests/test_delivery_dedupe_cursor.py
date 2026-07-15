import unittest
from src.delivery_dedupe_cursor import DeliveryDeduper
class DedupeTests(unittest.TestCase):
    def test_rejects_retry_in_same_worker(self):
        d=DeliveryDeduper(); self.assertTrue(d.accept("del-1")); self.assertFalse(d.accept("del-1"))
    def test_accepts_distinct_delivery(self):
        d=DeliveryDeduper(); self.assertTrue(d.accept("del-1")); self.assertTrue(d.accept("del-2"))
if __name__ == "__main__": unittest.main()
