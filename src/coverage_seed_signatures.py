"""Webhook signature verification with rotation support."""

import hashlib
import hmac


def _digest(payload, key):
    return hmac.new(key.encode(), payload, hashlib.sha256).hexdigest()


def verify_webhook_signature(payload, signature, primary_key, fallback_key=None):
    if hmac.compare_digest(_digest(payload, primary_key), signature):
        return True
    if fallback_key is not None:
        return hmac.compare_digest(_digest(payload, fallback_key), signature)
    return False
