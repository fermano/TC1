import unittest
from src.delivery_dedupe_cursor import DeliveryDeduper


class DedupeTests(unittest.TestCase):
    def test_rejects_retry_in_same_worker(self):
        d = DeliveryDeduper()
        self.assertTrue(d.accept("del-1"))
        self.assertFalse(d.accept("del-1"))

    def test_accepts_distinct_delivery(self):
        d = DeliveryDeduper()
        self.assertTrue(d.accept("del-1"))
        self.assertTrue(d.accept("del-2"))

    def test_accepts_same_ack_for_different_tenants(self):
        d = DeliveryDeduper()
        self.assertTrue(d.accept("ack-88", tenant_id="tenant-a"))
        self.assertTrue(d.accept("ack-88", tenant_id="tenant-b"))

    def test_rejects_same_ack_for_same_tenant_after_trimming(self):
        d = DeliveryDeduper()
        self.assertTrue(d.accept("ack-88", tenant_id=" tenant-a "))
        self.assertFalse(d.accept("ack-88", tenant_id="tenant-a"))

    def test_tenant_scoped_key_does_not_collide_with_legacy_global_scope(self):
        d = DeliveryDeduper()
        self.assertTrue(d.accept("ack-88"))
        self.assertTrue(d.accept("ack-88", tenant_id="tenant-a"))
        self.assertFalse(d.accept("ack-88"))

    def test_rejects_blank_tenant(self):
        d = DeliveryDeduper()
        with self.assertRaises(ValueError):
            d.accept("ack-88", tenant_id="  ")


if __name__ == "__main__":
    unittest.main()
