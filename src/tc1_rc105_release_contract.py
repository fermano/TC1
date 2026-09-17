"""RC105 release-row contract."""

def replay_row_key(tenant_id, route_id, delivery_id):
    return f"{tenant_id}:{route_id}:{delivery_id}"


def candidate_metadata(route_id):
    return {
        "artifact_stage": "rc105-candidate",
        "route_signature": f"route:{route_id}",
    }
