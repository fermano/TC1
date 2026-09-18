"""Earlier source-grouping prototype; implementation history only."""

def legacy_manifest_key(tenant_id, route_id, invoice_id, source):
    return f"{tenant_id}:{route_id}:{invoice_id}:{source}"


def legacy_source_metadata(route_id, source):
    return {
        "artifact_stage": "mainline-preview",
        "route_signature": f"route:{route_id}",
        "source_channel": source,
    }
