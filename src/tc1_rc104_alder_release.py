"""Alder partner replay rows for RC104."""

from src.tc1_rc104_release_contract import release_identity, release_metadata


def alder_release_row(tenant_id, route_id, invoice_id, payload, default_wait=240):
    raw = payload.get("ready_after")
    if raw is None or raw == "":
        raw = payload.get("readyAfter")
    if raw is None or raw == "":
        raw = default_wait
    wait_seconds = int(raw)
    return {
        "row_key": release_identity(tenant_id, route_id, invoice_id),
        "decision": "release" if wait_seconds == 0 else "wait",
        "wait_seconds": wait_seconds,
        **release_metadata(route_id),
    }
