"""RC-74 dispatch window helper.

The release branch uses route-scoped records. Older tenant-level delay helpers are
not safe to copy directly because the same tenant can have multiple route exports.
"""


def route_key(record):
    route = record.get("route_id") or record.get("legacy_route_id") or record.get("destination_id")
    return f"{record.get('tenant_id', 'unknown')}:{route or 'default'}"


def dispatch_window_seconds(record, workspace_default=300):
    if "window_seconds" in record and record.get("window_seconds") not in (None, ""):
        return int(record["window_seconds"])
    if "route_window_seconds" in record and record.get("route_window_seconds") not in (None, ""):
        return int(record["route_window_seconds"])
    return int(workspace_default)


def release_dispatch_record(record, workspace_default=300):
    return {
        "scope_key": route_key(record),
        "window_seconds": dispatch_window_seconds(record, workspace_default),
        "source": "rc74-route-scoped",
    }
