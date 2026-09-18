"""Current RC106 candidate-row contract."""

def manifest_key(tenant_id, route_id, invoice_id):
    return f"{tenant_id}:{route_id}:{invoice_id}"


def candidate_metadata(route_id):
    return {
        "artifact_stage": "rc106-candidate",
        "route_signature": f"route:{route_id}",
        "replay_generation": "d-9",
    }
