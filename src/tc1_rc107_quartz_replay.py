"""Quartz replay rows for the RC107 recovery."""

from src.tc1_rc107_replay_contract import (
    candidate_metadata,
    decode_persisted_key,
    replay_key,
)


def replay_rows(persisted_keys, events):
    rows = {}
    for persisted_key in persisted_keys:
        tenant_id, route_id, job_id, source = decode_persisted_key(persisted_key)
        rows[replay_key(tenant_id, route_id, job_id, source)] = {
            "disposition": "deliver",
            **candidate_metadata(route_id, source),
        }

    for event in events:
        key = replay_key(
            event["tenant_id"],
            event["route_id"],
            event["job_id"],
            event["source"],
        )
        if event["event_type"] == "retract":
            rows.pop(key, None)
        else:
            rows[key] = {
                "disposition": "deliver",
                **candidate_metadata(event["route_id"], event["source"]),
            }
    return rows
