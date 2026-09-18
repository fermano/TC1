"""Ash release record contract."""

def record_key(account_id, lane_id, request_id, origin):
    return f"{account_id}:{lane_id}:{request_id}:{origin}"


def decode_record_key(key):
    parts = key.split(":")
    if len(parts) == 3:
        return (*parts, "primary")
    return tuple(parts)


def release_context(lane_id, origin):
    return {
        "release": "ash-1",
        "lane": lane_id,
        "origin": origin,
    }
