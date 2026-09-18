from src.tc1_larch_entitlements import apply_partner_change


def test_active_change_adds_feature():
    assert apply_partner_change({"reports"}, {
        "account_state": "active",
        "feature": "forecasting",
    }) == {"reports", "forecasting"}


def test_inactive_change_does_not_add_feature():
    assert apply_partner_change({"reports"}, {
        "account_state": "closed",
        "feature": "forecasting",
    }) == {"reports"}
