"""RC-75 invoice gate helper.

RC-75 uses lane-scoped rows so one tenant can safely emit separate invoice
windows for bank, card, and email routes without overwriting each other.
"""


def lane_key(record):
    tenant = record.get("tenant_id") or "unknown"
    route = record.get("route_id") or record.get("legacy_route_id") or record.get("destination_id") or "default"
    invoice = record.get("invoice_id") or record.get("legacy_invoice_id") or "unassigned"
    return f"{tenant}:{route}:{invoice}"


def gate_seconds(record, default_seconds=45):
    for field in ("gate_seconds", "route_gate_seconds", "cancel_after_seconds", "gate_delay_seconds"):
        if record.get(field) not in (None, ""):
            return int(record[field])
    return int(default_seconds)


def invoice_gate_record(record, default_seconds=45):
    return {
        "lane_key": lane_key(record),
        "gate_seconds": gate_seconds(record, default_seconds),
        "source": "rc75-lane-scoped",
    }
