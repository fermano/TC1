"""Earlier source-isolated replay prototype; implementation history only."""

def source_key(tenant_id, route_id, job_id, source):
    return f"{tenant_id}:{route_id}:{job_id}:{source}"


def apply_source_event(rows, tenant_id, route_id, job_id, source, event_type):
    key = source_key(tenant_id, route_id, job_id, source)
    if event_type == "retract":
        rows.pop(key, None)
    else:
        rows[key] = "deliver"
    return rows
