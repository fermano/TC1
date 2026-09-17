"""Current RC104 release-row contract.

The release branch owns the route-distinct identity and the metadata emitted with
every candidate row. Intake prototypes cannot replace this contract.
"""

def release_identity(tenant_id, route_id, invoice_id):
    return f"{tenant_id}:{route_id}:{invoice_id}"


def release_metadata(route_id):
    return {
        "artifact_stage": "rc104-candidate",
        "route_signature": f"route:{route_id}",
        "release_channel": "rc104",
    }
