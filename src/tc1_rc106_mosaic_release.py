"""Mosaic manifest rows for the RC106 recovery."""

from src.tc1_rc106_manifest_contract import candidate_metadata, manifest_key


def _first_present_hold_seconds(payload, default_hold):
    for field in ("hold_seconds", "holdSeconds"):
        value = payload.get(field)
        if value is None:
            continue
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                continue
        return int(value)
    return int(default_hold)


def mosaic_manifest_row(tenant_id, route_id, invoice_id, source, payload, default_hold=180):
    hold_seconds = _first_present_hold_seconds(payload, default_hold)
    return {
        "row_key": manifest_key(tenant_id, route_id, invoice_id, source),
        "disposition": "emit" if hold_seconds == 0 else "hold",
        "hold_seconds": hold_seconds,
        **candidate_metadata(route_id, source),
    }
