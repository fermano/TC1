"""Audit-record projection with opt-in tenant metadata."""


def project_audit_record(event, include_tenant=False):
    projected = {"id": event["id"], "action": event["action"]}
    if include_tenant and event.get("tenant_id"):
        projected["tenant_id"] = event["tenant_id"].strip()
    return projected
