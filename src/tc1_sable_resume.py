"""Sable candidate packet resumption."""

from src.tc1_sable_contract import candidate_context, decode_packet_key, packet_key


def _send_after(event, default_seconds):
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
    return "native"


def _revision(event):
    value = event.get("revision", 0)
    if value is None or (isinstance(value, str) and not value.strip()):
        return 0
    return int(value)


def resume_packets(persisted_keys, events, default_seconds=90, artifact_ref="sable-rc-5"):
    packets = {}
    packet_revisions = {}
    for persisted_key in persisted_keys:
        account_id, lane_id, packet_id, origin = decode_packet_key(persisted_key)
        key = packet_key(account_id, lane_id, packet_id, origin)
        packet_revisions[key] = 0
        packets[key] = {
            "state": "queued",
            **candidate_context(lane_id, origin, artifact_ref),
        }

    for event in events:
        origin = _origin(event)
        key = packet_key(event["account_id"], event["lane_id"], event["packet_id"], origin)
        revision = _revision(event)
        if revision < packet_revisions.get(key, -1):
            continue
        packet_revisions[key] = revision
        if event["kind"] == "void":
            packets.pop(key, None)
            continue
        packets[key] = {
            "state": "queued",
            "send_after_seconds": _send_after(event, default_seconds),
            **candidate_context(event["lane_id"], origin, artifact_ref),
        }
    return packets
