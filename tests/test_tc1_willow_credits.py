from src.tc1_willow_credits import apply_adjustment


def test_omitted_mode_stacks_named_credit():
    assert apply_adjustment({"annual", "service"}, {
        "account_state": "active",
        "credit_id": "migration",
        "replaces_credit_id": "annual",
    }) == {"annual", "migration", "service"}


def test_explicit_amendment_removes_named_credit():
    assert apply_adjustment({"annual"}, {
        "account_state": "active",
        "credit_id": "migration",
        "replaces_credit_id": "annual",
        "adjustment_mode": "amendment",
    }) == {"migration"}
