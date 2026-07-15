import unittest
from src.delivery_owner_filter import filter_delivery_records
class OwnerFilterTests(unittest.TestCase):
    def setUp(self):
        self.rows=[{"id":1,"owner":"Billing  Ops"},{"id":2,"owner":"sales"},{"id":3,"owner":"billing ops"}]
    def test_none_means_no_filter(self): self.assertEqual(filter_delivery_records(self.rows,None),self.rows)
    def test_empty_means_no_records(self): self.assertEqual(filter_delivery_records(self.rows,[]),[])
    def test_normalized_matching_preserves_order_once(self):
        self.assertEqual([r["id"] for r in filter_delivery_records(self.rows,["billing ops"," Billing  Ops "])],[1,3])
if __name__ == "__main__": unittest.main()
