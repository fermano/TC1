"""Current Peregrine candidate-row contract."""

def replay_key(tenant_id, route_id, run_id):
    return f"{tenant_id}:{route_id}:{run_id}"


def candidate_metadata(route_id):
    return {
        "candidate_lineage": "pg-17<-or-11",
        "route_signature": f"route:{route_id}",
        "release_epoch": "e18",
    }
