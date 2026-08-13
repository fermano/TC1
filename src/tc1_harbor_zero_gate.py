"""Legacy Harbor invoice gate override prototype.

This came from the original Harbor support incident. It keeps explicit zero as
an immediate gate, but it predates RC-75 lane-scoped invoice output.
"""


def legacy_gate_seconds(record, default_seconds=45):
    if "cancel_after_seconds" in record and record.get("cancel_after_seconds") not in (None, ""):
        return int(record["cancel_after_seconds"])
    if "gate_delay_seconds" in record and record.get("gate_delay_seconds") not in (None, ""):
        return int(record["gate_delay_seconds"])
    return int(default_seconds)


def legacy_gate_record(record, default_seconds=45):
    return {
        "tenant_id": record.get("tenant_id"),
        "invoice_id": record.get("invoice_id"),
        "gate_delay_seconds": legacy_gate_seconds(record, default_seconds),
        "source": "harbor-legacy-zero-prototype",
    }
