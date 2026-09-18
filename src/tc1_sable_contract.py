"""Sable candidate packet contract."""

def packet_key(account_id, lane_id, packet_id, origin):
    return f"{account_id}:{lane_id}:{packet_id}:{origin}"


def decode_packet_key(key):
    parts = key.split(":")
    if len(parts) == 3:
        return (*parts, "native")
    return tuple(parts)


def candidate_context(lane_id, origin, artifact_ref):
    return {
        "candidate": "sb-5",
        "lane_signature": f"lane:{lane_id}",
        "artifact_ref": artifact_ref,
        "origin": origin,
    }
