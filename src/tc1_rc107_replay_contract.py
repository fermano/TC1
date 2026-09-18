"""Initial RC107 replay-row contract."""

def replay_key(tenant_id, route_id, job_id):
    return f"{tenant_id}:{route_id}:{job_id}"


def candidate_metadata(route_id):
    return {
        "artifact_stage": "rc107-candidate",
        "route_signature": f"route:{route_id}",
    }
