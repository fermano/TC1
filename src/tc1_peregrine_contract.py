"""Current Peregrine candidate-row contract."""

def replay_key(tenant_id, route_id, run_id, source=None):
    key = f"{tenant_id}:{route_id}:{run_id}"
    return key if source is None else f"{key}:{source}"


def decode_persisted_key(key):
    parts = key.split(":")
    if len(parts) == 3:
        return (*parts, "primary")
    return tuple(parts)


def candidate_metadata(route_id, source=None):
    metadata = {
        "candidate_lineage": "pg-17<-or-11",
        "route_signature": f"route:{route_id}",
        "release_epoch": "e18",
    }
    if source is not None:
        metadata["source_channel"] = source
    return metadata
