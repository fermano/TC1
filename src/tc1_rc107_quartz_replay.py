"""Partial RC107 Quartz replay recovery."""

from tc1_rc107_replay_contract import candidate_metadata, replay_key


def replay_rows(persisted_keys, events):
    rows = {key: {"disposition": "deliver"} for key in persisted_keys}
    for event in events:
        key = replay_key(event["tenant_id"], event["route_id"], event["job_id"])
        if event["event_type"] == "retract":
            rows.pop(key, None)
        else:
            rows[key] = {
                "disposition": "deliver",
                **candidate_metadata(event["route_id"]),
            }
    return rows
