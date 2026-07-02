import unittest

class ApprovalCacheReviewTests(unittest.TestCase):
    def test_policy_revision_invalidates_cached_approval(self):
        cached_revision = 17
        current_revision = 18
        self.assertEqual(cached_revision, current_revision, "stale approval remains accepted")

if __name__ == "__main__":
    unittest.main()
