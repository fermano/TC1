"""Partner hold reason helpers."""

_REASON_ALIASES = {
    "partner-paused": "partner_paused",
    "partner_paused": "partner_paused",
    "customer-paused": "customer_paused",
    "customer_paused": "customer_paused",
}


def partner_hold_reason(value):
    return _REASON_ALIASES.get(str(value or "").strip().lower(), "unknown")
