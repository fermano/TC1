import unittest
from src.delivery_summary_metadata import delivery_summary_with_source


class SummarySourceTests(unittest.TestCase):
    def test_default_shape_is_unchanged(self):
        self.assertEqual(
            delivery_summary_with_source(
                {
                    "owner": "ops",
                    "status": "sent",
                    "source": "api",
                    "source_label": "Partner retry",
                    "source_url": "https://hooks.example.test/callback",
                }
            ),
            {"owner": "ops", "status": "sent"},
        )

    def test_opt_in_trims_source(self):
        self.assertEqual(
            delivery_summary_with_source({"owner": "ops", "status": "sent", "source": " api "}, True)[
                "source"
            ],
            "api",
        )

    def test_opt_in_omits_blank_source(self):
        self.assertNotIn(
            "source",
            delivery_summary_with_source({"owner": "ops", "status": "sent", "source": "  "}, True),
        )

    def test_opt_in_prefers_display_label(self):
        self.assertEqual(
            delivery_summary_with_source(
                {
                    "owner": "ops",
                    "status": "sent",
                    "source_label": " Partner retry ",
                    "source_kind": "partner-retry",
                    "source": "legacy",
                    "source_url": "https://hooks.example.test/callback",
                },
                True,
            )["source"],
            "Partner retry",
        )

    def test_opt_in_uses_source_kind_before_legacy_source(self):
        self.assertEqual(
            delivery_summary_with_source(
                {
                    "owner": "ops",
                    "status": "sent",
                    "source_kind": "partner-retry",
                    "source": "legacy",
                },
                True,
            )["source"],
            "partner-retry",
        )

    def test_opt_in_omits_url_like_legacy_source(self):
        self.assertNotIn(
            "source",
            delivery_summary_with_source(
                {
                    "owner": "ops",
                    "status": "sent",
                    "source": "https://hooks.example.test/callback",
                    "source_url": "https://hooks.example.test/callback",
                },
                True,
            ),
        )

    def test_opt_in_skips_unsafe_display_label_for_safe_source_kind(self):
        self.assertEqual(
            delivery_summary_with_source(
                {
                    "owner": "ops",
                    "status": "sent",
                    "source_label": "https://hooks.example.test/callback",
                    "source_kind": "support-handoff",
                },
                True,
            )["source"],
            "support-handoff",
        )


if __name__ == "__main__":
    unittest.main()
