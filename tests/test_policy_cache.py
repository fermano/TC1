import unittest

from src.policy_cache import PolicySnapshotCache


class PolicySnapshotCacheTests(unittest.TestCase):
    def test_same_workspace_version_reuses_snapshot(self):
        cache = PolicySnapshotCache()
        loads = []

        def load():
            loads.append("load")
            return {"retry_budget": 3}

        first = cache.get_or_load("workspace-7", 12, load)
        second = cache.get_or_load("workspace-7", 12, load)

        self.assertIs(first, second)
        self.assertEqual(loads, ["load"])

    def test_new_workspace_version_loads_new_snapshot(self):
        cache = PolicySnapshotCache()
        versions = iter(({"retry_budget": 3}, {"retry_budget": 0}))

        first = cache.get_or_load("workspace-7", 12, lambda: next(versions))
        second = cache.get_or_load("workspace-7", 13, lambda: next(versions))

        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
