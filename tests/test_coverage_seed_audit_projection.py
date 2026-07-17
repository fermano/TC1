import unittest

from src.coverage_seed_audit_projection import project_audit_record


class AuditProjectionTests(unittest.TestCase):
    def test_opt_in_includes_trimmed_tenant(self):
        event = {"id": "evt-1", "action": "sent", "tenant_id": " tenant-7 "}
        self.assertEqual(
            project_audit_record(event, include_tenant=True),
            {"id": "evt-1", "action": "sent", "tenant_id": "tenant-7"},
        )

    def test_default_preserves_existing_shape(self):
        event = {"id": "evt-2", "action": "retried", "tenant_id": "tenant-8"}
        self.assertEqual(
            project_audit_record(event),
            {"id": "evt-2", "action": "retried"},
        )

    def test_opt_in_omits_missing_tenant(self):
        event = {"id": "evt-3", "action": "sent"}
        self.assertEqual(
            project_audit_record(event, include_tenant=True),
            {"id": "evt-3", "action": "sent"},
        )


if __name__ == "__main__":
    unittest.main()
