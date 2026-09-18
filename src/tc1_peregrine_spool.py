"""Peregrine partner-spool recovery."""

from src.tc1_peregrine_contract import (
    candidate_metadata,
    decode_persisted_key,
    replay_key,
)


def _dispatch_delay(event, default_delay):
    for field in ("dispatch_after", "dispatchAfter"):
        value = event.get(field)
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        return int(value)
    return default_delay


def restore_rows(persisted_keys, events, default_delay=180):
    rows = {}
    for persisted_key in persisted_keys:
        tenant_id, route_id, run_id, source = decode_persisted_key(persisted_key)
        rows[replay_key(tenant_id, route_id, run_id, source)] = {
            "state": "queued",
            **candidate_metadata(route_id, source),
        }

    for event in events:
        key = replay_key(
            event["tenant_id"],
            event["route_id"],
            event["run_id"],
            event["source"],
        )
        if event["event_type"] == "cancel":
            rows.pop(key, None)
        else:
            rows[key] = {
                "state": "queued",
                "delay_seconds": _dispatch_delay(event, default_delay),
                **candidate_metadata(event["route_id"], event["source"]),
            }
    return rows
