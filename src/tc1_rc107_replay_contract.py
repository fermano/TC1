"""Partial RC107 replay-row contract."""

def replay_key(tenant_id, route_id, job_id, source=None):
    key = f"{tenant_id}:{route_id}:{job_id}"
    return key if source is None else f"{key}:{source}"


def decode_persisted_key(key):
    parts = key.split(":")
    if len(parts) == 3:
        return (*parts, "primary")
    return tuple(parts)


def candidate_metadata(route_id, source=None):
    metadata = {
        "artifact_stage": "rc107-candidate",
        "route_signature": f"route:{route_id}",
    }
    if source is not None:
        metadata["source_channel"] = source
    return metadata
