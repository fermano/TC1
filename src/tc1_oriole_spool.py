"""Oriole resumption attempt."""

def oriole_rows(events, default_delay=180):
    rows = {}
    for event in events:
        raw = event.get("dispatch_after") or event.get("dispatchAfter") or default_delay
        key = f"{event['tenant_id']}:{event['route_id']}:{event['run_id']}"
        if event["event_type"] == "cancel":
            rows.pop(key, None)
        else:
            rows[key] = {"delay": int(raw), "state": "queued"}
    return rows
