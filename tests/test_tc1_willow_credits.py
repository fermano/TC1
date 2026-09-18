from src.tc1_willow_credits import apply_adjustment


def test_active_adjustment_adds_credit():
    assert apply_adjustment({"annual"}, {
        "account_state": "active",
        "credit_id": "migration",
    }) == {"annual", "migration"}


def test_inactive_adjustment_keeps_existing_credits():
    assert apply_adjustment({"annual"}, {
        "account_state": "closed",
        "credit_id": "migration",
    }) == {"annual"}
