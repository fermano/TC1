import unittest

from src.ticket_workflow_seed import (
    DEFAULT_OWNER,
    delivery_summary,
    filter_delivery_records,
    normalize_delivery_owner,
)


class TicketWorkflowSeedTests(unittest.TestCase):
    def test_blank_owner_uses_default(self):
        self.assertEqual(normalize_delivery_owner(None), DEFAULT_OWNER)

    def test_owner_is_trimmed_and_lowercased(self):
        self.assertEqual(normalize_delivery_owner(" Billing-Ops "), "billing-ops")

    def test_owner_collapses_repeated_unicode_whitespace(self):
        self.assertEqual(
            normalize_delivery_owner("  Billing\t\u2003Ops\n"),
            "billing ops",
        )

    def test_owner_preserves_punctuation(self):
        self.assertEqual(normalize_delivery_owner("Billing/OnCall"), "billing/oncall")

    def test_missing_owner_filter_returns_all_records(self):
        records = [{"owner": "alpha"}, {"owner": "beta"}]
        self.assertEqual(filter_delivery_records(records), records)

    def test_empty_owner_filter_returns_no_records(self):
        self.assertEqual(filter_delivery_records([{"owner": "alpha"}], []), [])

    def test_owner_filter_canonicalizes_deduplicates_and_preserves_order(self):
        records = [
            {"id": 1, "owner": "Beta Ops"},
            {"id": 2, "owner": "alpha"},
            {"id": 3, "owner": " beta\t ops "},
            {"id": 4, "owner": "gamma"},
        ]
        self.assertEqual(
            filter_delivery_records(records, [" BETA OPS ", "beta\u2003ops"]),
            [records[0], records[2]],
        )

    def test_owner_filter_matches_blank_owner_to_default(self):
        records = [{"owner": None}, {"owner": "alpha"}]
        self.assertEqual(filter_delivery_records(records, [DEFAULT_OWNER]), [records[0]])

    def test_summary_contains_existing_fields(self):
        self.assertEqual(
            delivery_summary({"owner": " Billing-Ops ", "status": "queued"}),
            {"owner": "billing-ops", "status": "queued"},
        )


if __name__ == "__main__":
    unittest.main()
