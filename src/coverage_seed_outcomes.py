"""Shared delivery-outcome categorization."""

SUCCESS_OUTCOMES = {"sent", "delivered"}
RETRY_OUTCOMES = {"retry", "rate_limited"}
DROP_OUTCOMES = {"rejected", "expired"}


def categorize_delivery_outcome(value):
    normalized = (value or "").strip().lower()
    if normalized in SUCCESS_OUTCOMES:
        return "success"
    if normalized in RETRY_OUTCOMES:
        return "retry"
    if normalized in DROP_OUTCOMES:
        return "dropped"
    return "unknown"
