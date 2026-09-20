from src.vesper_preview import preview_includes_settlement
from src.vesper_reconciliation import reconciliation_settlement_reference
from src.vesper_settlement_export import vesper_settlement_reference


def test_committed_structured_settlement_is_exported_to_rc1_consumers():
    metadata = {"settlement": {"token": "vs-120", "state": "committed"}}

    assert vesper_settlement_reference(metadata) == "vs-120"
    assert preview_includes_settlement(metadata) is True
    assert reconciliation_settlement_reference(metadata) == "vs-120"


def test_non_committed_or_missing_structured_settlement_is_not_exported():
    assert vesper_settlement_reference(
        {"settlement": {"token": "vs-120", "state": "prepared"}}
    ) is None
    assert vesper_settlement_reference({}) is None
