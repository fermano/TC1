"""Willow candidate credit-adjustment behavior."""

def apply_adjustment(active_credit_ids, adjustment):
    credits = set(active_credit_ids)
    if adjustment.get("account_state") != "active":
        return credits
    credits.add(adjustment["credit_id"])
    return credits
