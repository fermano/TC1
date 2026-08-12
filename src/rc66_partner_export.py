"""Partner pilot export row selection for RC-66.

The export job writes a compact partner-facing CSV from internal event rows.
The pilot harness imports this module directly when comparing package contents.
"""

SUPPORTED_EVENT_TYPES = {"shipment", "retry"}
EXPORTABLE_STATES = {"posted", "ready"}


def _normalize(value):
    return str(value or "").strip().lower().replace(" ", "_")


def build_partner_export_rows(events):
    """Return exportable partner rows in stable first-seen order."""
    rows = []
    seen = set()

    for event in events:
        partner = _normalize(event.get("partner"))
        if partner not in {"atlas", "nova"}:
            continue

        event_type = _normalize(event.get("event_type"))
        if event_type not in SUPPORTED_EVENT_TYPES:
            continue

        state = _normalize(event.get("state"))
        if state not in EXPORTABLE_STATES:
            continue

        if event.get("dry_run"):
            continue

        key = (event.get("tenant_id"), partner, event.get("external_id"), event_type)
        if key in seen:
            continue
        seen.add(key)

        rows.append(
            {
                "tenant_id": event.get("tenant_id"),
                "partner": partner,
                "external_id": event.get("external_id"),
                "event_type": event_type,
                "amount_cents": event.get("amount_cents", 0),
            }
        )

    return rows
