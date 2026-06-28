"""Redaction allowlist proposal.

New key categories default to visible, which is the review concern.
"""
SAFE_KEYS = {"provider", "region"}

def redact_key_name(name: str) -> str:
    return name if name in SAFE_KEYS else "[redacted]"
