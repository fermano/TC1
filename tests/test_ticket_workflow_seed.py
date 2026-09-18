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

    def test_blank_owner_selection_matches_blank_record_through_default(self):
        records = [{"owner": None}, {"owner": "alpha"}]
        self.assertEqual(filter_delivery_records(records, [None]), [records[0]])

    def test_summary_contains_existing_fields(self):
        self.assertEqual(
            delivery_summary(
                {
                    "owner": " Billing-Ops ",
                    "status": "queued",
                    "source": "api",
                    "lane": "retry",
                }
            ),
            {"owner": "billing-ops", "status": "queued"},
        )

    def test_summary_includes_lane_when_opted_in(self):
        self.assertEqual(
            delivery_summary(
                {"owner": "alpha", "status": "queued", "lane": " Retry "},
                include_lane=True,
            ),
            {"owner": "alpha", "status": "queued", "lane": "retry"},
        )

    def test_summary_uses_legacy_lane_alias_when_canonical_absent(self):
        self.assertEqual(
            delivery_summary(
                {
                    "owner": "alpha",
                    "status": "queued",
                    "delivery_lane": "manual-replay",
                },
                include_lane=True,
            ),
            {"owner": "alpha", "status": "queued", "lane": "manual-replay"},
        )

    def test_summary_defaults_lane_to_primary_when_opted_in(self):
        self.assertEqual(
            delivery_summary(
                {"owner": "alpha", "status": "queued"},
                include_lane=True,
            ),
            {"owner": "alpha", "status": "queued", "lane": "primary"},
        )

    def test_summary_rejects_blank_canonical_lane_without_alias_fallback(self):
        with self.assertRaisesRegex(ValueError, "lane must"):
            delivery_summary(
                {
                    "owner": "alpha",
                    "status": "queued",
                    "lane": "  ",
                    "delivery_lane": "retry",
                },
                include_lane=True,
            )

    def test_summary_rejects_malformed_legacy_lane_alias(self):
        with self.assertRaisesRegex(ValueError, "delivery_lane must"):
            delivery_summary(
                {
                    "owner": "alpha",
                    "status": "queued",
                    "delivery_lane": "retry_lane",
                },
                include_lane=True,
            )

    def test_summary_includes_trimmed_source_when_opted_in(self):
        self.assertEqual(
            delivery_summary(
                {"owner": "alpha", "status": "queued", "source": "  api  "},
                include_source=True,
            ),
            {"owner": "alpha", "status": "queued", "source": "api"},
        )

    def test_summary_uses_safe_source_label_when_opted_in(self):
        self.assertEqual(
            delivery_summary(
                {
                    "owner": "alpha",
                    "status": "queued",
                    "source_label": "Support handoff",
                    "source_kind": "partner-retry",
                    "source": "https://hooks.example.test/callback",
                },
                include_source=True,
            ),
            {"owner": "alpha", "status": "queued", "source": "Support handoff"},
        )

    def test_summary_can_include_source_and_lane_together(self):
        self.assertEqual(
            delivery_summary(
                {
                    "owner": "alpha",
                    "status": "queued",
                    "source_label": "Support handoff",
                    "lane": "retry",
                },
                include_source=True,
                include_lane=True,
            ),
            {
                "owner": "alpha",
                "status": "queued",
                "lane": "retry",
                "source": "Support handoff",
            },
        )

    def test_summary_omits_blank_or_missing_source_when_opted_in(self):
        for record in (
            {"owner": "alpha", "status": "queued"},
            {"owner": "alpha", "status": "queued", "source": "   "},
            {"owner": "alpha", "status": "queued", "source": None},
            {
                "owner": "alpha",
                "status": "queued",
                "source": "https://hooks.example.test/callback",
            },
        ):
            with self.subTest(record=record):
                self.assertEqual(
                    delivery_summary(record, include_source=True),
                    {"owner": "alpha", "status": "queued"},
                )


if __name__ == "__main__":
    unittest.main()
