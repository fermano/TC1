"""Juniper candidate plan-change behavior."""

def apply_change(active_plan_ids, incoming_change):
    plans = set(active_plan_ids)
    if incoming_change.get("account_state") != "active":
        return plans
    if incoming_change.get("replace_scope") in (None, "same-product"):
        plans.discard(incoming_change.get("replaces_plan_id"))
    plans.add(incoming_change["plan_id"])
    return plans
