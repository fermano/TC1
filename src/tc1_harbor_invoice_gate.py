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
    if record.get("gate_seconds") not in (None, ""):
        return int(record["gate_seconds"])
    if record.get("route_gate_seconds") not in (None, ""):
        return int(record["route_gate_seconds"])
    return int(default_seconds)


def invoice_gate_record(record, default_seconds=45):
    return {
        "lane_key": lane_key(record),
        "gate_seconds": gate_seconds(record, default_seconds),
        "source": "rc75-lane-scoped",
    }
