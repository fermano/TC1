from src.tc1_juniper_plan_change import apply_change


def test_unspecified_scope_keeps_the_named_existing_plan():
    assert apply_change({"pro", "storage"}, {
        "account_state": "active",
        "plan_id": "pro-v2",
        "replaces_plan_id": "pro",
    }) == {"pro", "pro-v2", "storage"}


def test_explicit_same_product_scope_replaces_existing_plan():
    assert apply_change({"pro"}, {
        "account_state": "active",
        "plan_id": "pro-v2",
        "replaces_plan_id": "pro",
        "replace_scope": "same-product",
    }) == {"pro-v2"}
