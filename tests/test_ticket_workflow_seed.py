import unittest

from src.ticket_workflow_seed import DEFAULT_OWNER, delivery_summary, normalize_delivery_owner


class TicketWorkflowSeedTests(unittest.TestCase):
    def test_blank_owner_uses_default(self):
        self.assertEqual(normalize_delivery_owner(None), DEFAULT_OWNER)

    def test_owner_is_trimmed_and_lowercased(self):
        self.assertEqual(normalize_delivery_owner(" Billing-Ops "), "billing-ops")

    def test_summary_contains_existing_fields(self):
        self.assertEqual(
            delivery_summary({"owner": " Billing-Ops ", "status": "queued"}),
            {"owner": "billing-ops", "status": "queued"},
        )


if __name__ == "__main__":
    unittest.main()
