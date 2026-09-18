"""Ash release record contract."""

def record_key(account_id, lane_id, request_id, origin):
    return f"{account_id}:{lane_id}:{request_id}:{origin}"


def decode_record_key(key):
    parts = key.split(":")
    if len(parts) == 3:
        return (*parts, "primary")
    return tuple(parts)


def release_context(lane_id, origin, artifact_ref):
    return {
        "release": "ash-2",
        "record_shape": "v2",
        "lane": lane_id,
        "artifact_ref": artifact_ref,
        "origin": origin,
    }
