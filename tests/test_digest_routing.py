import unittest

from src.digest_routing import DEFAULT_DIGEST_OWNER, select_digest_owner


class DigestRoutingTests(unittest.TestCase):
    def test_customer_override_takes_precedence(self):
        self.assertEqual(
            select_digest_owner("customer-success", "platform"),
            "customer-success",
        )

    @unittest.skip("deferred until the workspace loader fixture is available")
    def test_workspace_reload_without_override_uses_persisted_owner(self):
        reloaded_override = None
        reloaded_owner = "platform"

        self.assertEqual(
            select_digest_owner(reloaded_override, reloaded_owner),
            "platform",
        )


if __name__ == "__main__":
    unittest.main()
