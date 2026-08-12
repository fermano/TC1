"""Failover route selection for RC-68 package builds."""

READY_STATES = {"ready", "queued"}
SUPPORTED_EVENTS = {"delivery", "retry"}
SUPPORTED_REGIONS = {"us", "eu", "apac"}


def _normalize(value):
    return str(value or "").strip().lower().replace(" ", "_")


def _route_region(event):
    region = _normalize(event.get("region"))
    if region in SUPPORTED_REGIONS:
        return region
    return "global"


def build_failover_routes(events):
    """Return failover route rows in stable first-seen order."""
    rows = []
    seen = set()

    for event in events:
        state = _normalize(event.get("state"))
        if state not in READY_STATES:
            continue

        event_type = _normalize(event.get("event_type"))
        if event_type not in SUPPORTED_EVENTS:
            continue

        key = (event.get("tenant_id"), event.get("delivery_id"), event_type)
        if key in seen:
            continue
        seen.add(key)

        rows.append(
            {
                "tenant_id": event.get("tenant_id"),
                "delivery_id": event.get("delivery_id"),
                "event_type": event_type,
                "route_region": _route_region(event),
            }
        )

    return rows
