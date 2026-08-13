"""Lagoon dispatch delay override prototype.

This prototype came from the original Lagoon customer incident. It preserves an
explicit zero-delay override, but it uses the old tenant-level output shape.
"""


def dispatch_delay_seconds(record, workspace_default=300):
    if "delay_seconds" in record and record.get("delay_seconds") not in (None, ""):
        return int(record["delay_seconds"])
    if "send_after_seconds" in record and record.get("send_after_seconds") not in (None, ""):
        return int(record["send_after_seconds"])
    return int(workspace_default)


def lagoon_dispatch_record(record, workspace_default=300):
    return {
        "tenant_id": record.get("tenant_id"),
        "delay_seconds": dispatch_delay_seconds(record, workspace_default),
        "source": "lagoon-flat-prototype",
    }
