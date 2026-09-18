from src.tc1_larch_entitlements import apply_partner_change


def test_omitted_scope_keeps_the_named_feature():
    assert apply_partner_change({"reports", "exports"}, {
        "account_state": "active",
        "feature": "forecasting",
        "replaces_feature": "reports",
    }) == {"reports", "forecasting", "exports"}


def test_explicit_replacement_scope_removes_named_feature():
    assert apply_partner_change({"reports"}, {
        "account_state": "active",
        "feature": "forecasting",
        "replaces_feature": "reports",
        "change_scope": "replacement",
    }) == {"forecasting"}
