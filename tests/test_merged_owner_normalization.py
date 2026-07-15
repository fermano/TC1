import unittest
from src.ticket_workflow_seed import DEFAULT_OWNER, normalize_delivery_owner
class OwnerNormalizationTests(unittest.TestCase):
    def test_collapses_internal_whitespace(self):
        self.assertEqual(normalize_delivery_owner("Billing  Ops"), "billing ops")
    def test_collapses_unicode_whitespace(self):
        self.assertEqual(normalize_delivery_owner("Billing\u00a0\tOps"), "billing ops")
    def test_preserves_separators(self):
        self.assertEqual(normalize_delivery_owner("Billing/OnCall"), "billing/oncall")
    def test_blank_still_uses_default(self):
        self.assertEqual(normalize_delivery_owner(" \t "), DEFAULT_OWNER)
if __name__ == "__main__": unittest.main()
