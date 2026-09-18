"""Ash release replay behavior."""

from src.tc1_ash_contract import decode_record_key, record_key, release_context


def _delay(event, default_seconds):
    for field in ("send_after", "sendAfter"):
        value = event.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        return int(value)
    return default_seconds


def _revision(event):
    return int(event.get("revision", 0))


def restore_records(persisted_keys, events, default_seconds=75):
    records = {}
    for persisted_key in persisted_keys:
        account_id, lane_id, request_id, origin = decode_record_key(persisted_key)
        records[record_key(account_id, lane_id, request_id, origin)] = {
            "state": "queued",
            "revision": 0,
            **release_context(lane_id, origin),
        }

    for event in events:
        key = record_key(
            event["account_id"], event["lane_id"], event["request_id"], event["origin"]
        )
        if _revision(event) < records.get(key, {}).get("revision", -1):
            continue
        if event["kind"] == "void":
            records.pop(key, None)
            continue
        records[key] = {
            "state": "queued",
            "revision": _revision(event),
            "delay_seconds": _delay(event, default_seconds),
            **release_context(event["lane_id"], event["origin"]),
        }
    return records
