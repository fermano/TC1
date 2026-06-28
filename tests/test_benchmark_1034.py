import unittest

class FailoverResumeSeedTests(unittest.TestCase):
    def test_resume_does_not_drop_buffered_events(self):
        buffered_before_failover = 12
        restored_after_failover = 0
        self.assertEqual(restored_after_failover, buffered_before_failover)

if __name__ == "__main__":
    unittest.main()
