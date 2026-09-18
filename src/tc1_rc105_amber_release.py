"""Amber replay disposition rows for RC105."""

from src.tc1_rc105_release_contract import candidate_metadata, replay_row_key


def amber_replay_row(tenant_id, route_id, delivery_id, payload, default_wait=180):
    raw = payload.get("retry_window")
    if raw is None or raw == "":
        raw = payload.get("retryWindow")
    if raw is None or raw == "":
        raw = default_wait
    retry_seconds = int(raw)
    return {
        "row_key": replay_row_key(tenant_id, route_id, delivery_id),
        "disposition": "dispatch" if retry_seconds == 0 else "defer",
        "retry_seconds": retry_seconds,
        **candidate_metadata(route_id),
    }
