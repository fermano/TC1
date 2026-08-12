"""Billing export candidate selection for RC-65.

The release-room replay harness imports this directly to compare candidate rows
against the packaged billing artifact.
"""

SUPPORTED_EVENT_TYPES = {"delivery", "retry"}
NON_BILLABLE_STATES = {"void", "refunded", "test"}


def _normalize(value):
    return str(value or "").strip().lower().replace(" ", "_")


def _is_test_mode(event):
    return _normalize(event.get("mode")) in {"test", "test_mode"}


def build_billing_candidates(events):
    """Return billable events in stable first-seen order.

    Older producers may omit environment metadata. Those rows remain eligible
    unless another explicit non-billable signal is present.
    """
    candidates = []
    seen = set()

    for event in events:
        event_type = _normalize(event.get("event_type"))
        if event_type not in SUPPORTED_EVENT_TYPES:
            continue

        state = _normalize(event.get("state"))
        if state in NON_BILLABLE_STATES:
            continue

        if _is_test_mode(event):
            continue

        if not event.get("billable", True):
            continue

        key = (event.get("tenant_id"), event.get("event_id"), event_type)
        if key in seen:
            continue
        seen.add(key)

        candidates.append(
            {
                "tenant_id": event.get("tenant_id"),
                "event_id": event.get("event_id"),
                "event_type": event_type,
                "amount_cents": event.get("amount_cents", 0),
            }
        )

    return candidates
