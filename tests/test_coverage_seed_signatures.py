import hashlib
import hmac
import unittest

from src.coverage_seed_signatures import verify_webhook_signature


class WebhookSignatureTests(unittest.TestCase):
    def test_primary_key_accepts_valid_signature(self):
        payload = b"{\"delivery\": 41}"
        signature = hmac.new(b"primary", payload, hashlib.sha256).hexdigest()
        self.assertTrue(verify_webhook_signature(payload, signature, "primary"))

    def test_primary_key_rejects_invalid_signature(self):
        self.assertFalse(verify_webhook_signature(b"payload", "invalid", "primary"))


if __name__ == "__main__":
    unittest.main()
