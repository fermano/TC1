from src.tc1_willow_credits import apply_adjustment


def test_omitted_mode_amends_named_credit():
    assert apply_adjustment({"annual", "service"}, {
        "account_state": "active",
        "credit_id": "migration",
        "replaces_credit_id": "annual",
    }) == {"migration", "service"}


def test_explicit_stack_keeps_named_credit():
    assert apply_adjustment({"annual"}, {
        "account_state": "active",
        "credit_id": "migration",
        "replaces_credit_id": "annual",
        "adjustment_mode": "stack",
    }) == {"annual", "migration"}
