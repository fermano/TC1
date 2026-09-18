"""Current RC106 candidate-row contract."""

def manifest_key(tenant_id, route_id, invoice_id, source=None):
    key = f"{tenant_id}:{route_id}:{invoice_id}"
    return key if source is None else f"{key}:{source}"


def candidate_metadata(route_id, source=None):
    metadata = {
        "artifact_stage": "rc106-candidate",
        "route_signature": f"route:{route_id}",
        "replay_generation": "d-9",
    }
    if source is not None:
        metadata["source_channel"] = source
    return metadata
