"""Willow candidate credit-adjustment behavior."""

def apply_adjustment(active_credit_ids, adjustment):
    credits = set(active_credit_ids)
    if adjustment.get("account_state") != "active":
        return credits
    if adjustment.get("adjustment_mode") == "amendment":
        credits.discard(adjustment.get("replaces_credit_id"))
    credits.add(adjustment["credit_id"])
    return credits
