"""Digest-facing escalation reason normalization."""


def digest_reason(value):
    text = str(value or "").strip().lower().replace("-", "_")
    if text == "customer_paused":
        return "customer_paused"
    if text == "manual_hold":
        return "manual_hold"
    return text
