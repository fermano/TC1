from src.vesper_preview import preview_includes_settlement
from src.vesper_reconciliation import reconciliation_settlement_reference
from src.vesper_settlement_export import vesper_settlement_reference


def test_legacy_committed_settlement_is_preserved_for_rc1_consumers():
    metadata = {"settlement_token": "vs-118", "settlement_phase": "committed"}

    assert vesper_settlement_reference(metadata) == "vs-118"
    assert preview_includes_settlement(metadata) is True
    assert reconciliation_settlement_reference(metadata) == "vs-118"


def test_committed_structured_settlement_fills_a_missing_legacy_value():
    metadata = {"settlement": {"token": "vs-120", "state": "committed"}}

    assert vesper_settlement_reference(metadata) == "vs-120"


def test_non_committed_structured_settlement_is_not_exported_without_legacy():
    assert vesper_settlement_reference(
        {"settlement": {"token": "vs-120", "state": "prepared"}}
    ) is None
