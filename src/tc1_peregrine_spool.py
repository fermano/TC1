"""Partial Peregrine partner-spool recovery."""

from tc1_peregrine_contract import candidate_metadata, replay_key


def restore_rows(persisted_keys, events, default_delay=180):
    rows = {key: {"state": "queued"} for key in persisted_keys}
    for event in events:
        raw = event.get("dispatch_after", event.get("dispatchAfter", default_delay)) or default_delay
        key = replay_key(event["tenant_id"], event["route_id"], event["run_id"])
        if event["event_type"] == "cancel":
            rows.pop(key, None)
        else:
            rows[key] = {
                "state": "queued",
                "delay_seconds": int(raw),
                **candidate_metadata(event["route_id"]),
            }
    return rows
