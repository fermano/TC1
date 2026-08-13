import pytest

from src.seed_owner_filter import filter_delivery_records


def test_none_owner_filter_preserves_all_records_in_order():
    records = [
        {"owner": "payments", "id": "a"},
        {"owner": "risk", "id": "b"},
    ]

    assert filter_delivery_records(records) == records


def test_populated_owner_filter_is_case_insensitive_and_preserves_order():
    records = [
        {"owner": "Payments", "id": "a"},
        {"owner": "risk", "id": "b"},
        {"owner": "PAYMENTS", "id": "c"},
    ]

    assert filter_delivery_records(records, owners=["payments"]) == [
        records[0],
        records[2],
    ]


@pytest.mark.skip(reason="empty-list semantics awaiting product decision")
def test_empty_owner_filter_contract():
    assert filter_delivery_records(
        [{"owner": "payments", "id": "a"}],
        owners=[],
    ) == []
