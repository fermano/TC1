import unittest

class AuditRegionMetricsSeedTests(unittest.TestCase):
    def test_region_dimension_is_present(self):
        metric = {"region": "sa-east-1", "events": 3}
        self.assertEqual(metric["region"], "sa-east-1")

if __name__ == "__main__":
    unittest.main()
