import pytest

from src.workspace_policy import retry_budget_from_record


@pytest.mark.parametrize("record", ({}, {"retry_budget": None}))
def test_missing_retry_budget_inherits_workspace_default(record):
    assert retry_budget_from_record(record, default=3) == 3


def test_explicit_zero_retry_budget_survives_policy_reload():
    assert retry_budget_from_record({"retry_budget": 0}, default=3) == 0


def test_positive_retry_budget_survives_policy_reload():
    assert retry_budget_from_record({"retry_budget": 2}, default=3) == 2
