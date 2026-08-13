"""Operator-facing hold reason normalization."""

_REASON_LABELS = {
    "customer_paused": "Customer paused",
    "customer-paused": "Customer paused",
    "manual_hold": "Manual hold",
    "manual-hold": "Manual hold",
}


def operator_hold_reason(value):
    normalized = str(value or "").strip().lower()
    return _REASON_LABELS.get(normalized, normalized.replace("_", " ").title())
