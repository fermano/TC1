from src.vesper_preview import preview_includes_settlement
from src.vesper_reconciliation import reconciliation_settlement_reference
from src.vesper_settlement_export import vesper_settlement_reference


def test_legacy_committed_settlement_is_exported_to_rc1_consumers():
    metadata = {"settlement_token": "vs-118", "settlement_phase": "committed"}

    assert vesper_settlement_reference(metadata) == "vs-118"
    assert preview_includes_settlement(metadata) is True
    assert reconciliation_settlement_reference(metadata) == "vs-118"


def test_blank_or_non_committed_legacy_settlement_is_not_exported():
    assert vesper_settlement_reference(
        {"settlement_token": " ", "settlement_phase": "committed"}
    ) is None
    assert vesper_settlement_reference(
        {"settlement_token": "vs-118", "settlement_phase": "prepared"}
    ) is None
