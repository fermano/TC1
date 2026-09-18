"""Larch candidate entitlement-change behavior."""

def apply_partner_change(active_features, change):
    features = set(active_features)
    if change.get("account_state") != "active":
        return features
    features.add(change["feature"])
    return features
