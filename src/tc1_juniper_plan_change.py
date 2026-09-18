"""Juniper candidate plan-change behavior."""

def apply_change(active_plan_ids, incoming_change):
    if incoming_change.get("account_state") != "active":
        return set(active_plan_ids)
    return set(active_plan_ids) | {incoming_change["plan_id"]}
