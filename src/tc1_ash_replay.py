"""Ash release replay behavior."""

from src.tc1_ash_contract import decode_record_key, record_key, release_context


def _delay(event, default_seconds):
    for field in ("send_after", "sendAfter"):
        value = event.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        return int(value)
    return default_seconds


def _origin(event):
    for field in ("origin", "originId"):
        value = event.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        return value
    return "primary"


def _revision(event):
    value = event.get("revision", 0)
    if value is None or (isinstance(value, str) and not value.strip()):
        return 0
    return int(value)


def restore_records(persisted_keys, events, default_seconds=75, artifact_ref="ash-rc-2"):
    records = {}
    record_revisions = {}
    for persisted_key in persisted_keys:
        account_id, lane_id, request_id, origin = decode_record_key(persisted_key)
        key = record_key(account_id, lane_id, request_id, origin)
        record_revisions[key] = 0
        records[key] = {
            "state": "queued",
            **release_context(lane_id, origin, artifact_ref),
        }

    for event in events:
        origin = _origin(event)
        key = record_key(event["account_id"], event["lane_id"], event["request_id"], origin)
        revision = _revision(event)
        if revision < record_revisions.get(key, -1):
            continue
        record_revisions[key] = revision
        if event["kind"] == "void":
            records.pop(key, None)
            continue
        records[key] = {
            "state": "queued",
            "delay_seconds": _delay(event, default_seconds),
            **release_context(event["lane_id"], origin, artifact_ref),
        }
    return records
