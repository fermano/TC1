"""Sable candidate packet resumption."""

from src.tc1_sable_contract import candidate_context, decode_packet_key, packet_key


def _send_after(event, default_seconds):
    for field in ("send_after", "sendAfter"):
        value = event.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            continue
        return int(value)
    return default_seconds


def resume_packets(persisted_keys, events, default_seconds=90, artifact_ref="sable-rc-5"):
    packets = {}
    for persisted_key in persisted_keys:
        account_id, lane_id, packet_id, origin = decode_packet_key(persisted_key)
        packets[packet_key(account_id, lane_id, packet_id, origin)] = {
            "state": "queued",
            **candidate_context(lane_id, origin, artifact_ref),
        }

    for event in events:
        key = packet_key(
            event["account_id"], event["lane_id"], event["packet_id"], event["origin"]
        )
        if event["kind"] == "void":
            packets.pop(key, None)
            continue
        packets[key] = {
            "state": "queued",
            "send_after_seconds": _send_after(event, default_seconds),
            **candidate_context(event["lane_id"], event["origin"], artifact_ref),
        }
    return packets
