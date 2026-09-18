from src.tc1_juniper_plan_change import apply_change


def test_active_change_adds_the_requested_plan():
    assert apply_change({"pro"}, {
        "account_state": "active",
        "plan_id": "analytics",
    }) == {"pro", "analytics"}


def test_inactive_account_keeps_existing_plans():
    assert apply_change({"pro"}, {
        "account_state": "closed",
        "plan_id": "analytics",
    }) == {"pro"}
