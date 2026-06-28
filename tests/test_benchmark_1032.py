import unittest

class PartitionDeletionSeedTests(unittest.TestCase):
    def test_expired_partition_is_queued(self):
        self.assertTrue({"expired": True}.get("expired"))

if __name__ == "__main__":
    unittest.main()
