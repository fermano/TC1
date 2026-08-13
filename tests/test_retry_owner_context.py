from src.retry_owner_context import owner_for_attempt


def test_retry_uses_operator_override():
    assert owner_for_attempt("routing-default", "ops-east") == "ops-east"


def test_retry_without_override_uses_original_owner():
    assert owner_for_attempt("routing-default") == "routing-default"
