import pytest

from src.release_manifest_checksum import (
    clear_manifest_checksum_cache,
    manifest_checksum,
)


def test_identical_retry_payload_reuses_checksum():
    clear_manifest_checksum_cache()
    rows = [{"invoice_id": "inv-1042", "amount": 11900}]

    first = manifest_checksum("manifest-20260613", rows)
    reconstructed = [{"amount": 11900, "invoice_id": "inv-1042"}]
    second = manifest_checksum("manifest-20260613", reconstructed)

    assert second == first


def test_caller_mutation_does_not_change_cached_binding():
    clear_manifest_checksum_cache()
    rows = [{"invoice_id": "inv-1042", "amount": 11900}]

    expected = manifest_checksum("manifest-20260613", rows)
    rows.append({"invoice_id": "inv-1043", "amount": 7200})

    assert manifest_checksum(
        "manifest-20260613",
        [{"amount": 11900, "invoice_id": "inv-1042"}],
    ) == expected


@pytest.mark.parametrize(
    "changed_rows",
    [
        [{"invoice_id": "inv-1042", "amount": 11900}],
        [{"invoice_id": "inv-1042", "amount": 11901}],
        [{"invoice_id": "inv-1043"}, {"invoice_id": "inv-1042", "amount": 11900}],
        [
            {"invoice_id": "inv-1042", "amount": 11900},
            {"invoice_id": "inv-1042", "amount": 11900},
        ],
    ],
    ids=["row-count", "field-value", "row-order", "duplicate-occurrence"],
)
def test_reusing_manifest_id_with_different_payload_raises(changed_rows):
    clear_manifest_checksum_cache()
    original_rows = [
        {"invoice_id": "inv-1042", "amount": 11900},
        {"invoice_id": "inv-1043"},
    ]
    manifest_checksum("manifest-20260613", original_rows)

    with pytest.raises(ValueError, match="already bound"):
        manifest_checksum("manifest-20260613", changed_rows)


def test_conflict_does_not_replace_original_binding():
    clear_manifest_checksum_cache()
    original_rows = [{"invoice_id": "inv-1042", "amount": 11900}]
    expected = manifest_checksum("manifest-20260613", original_rows)

    with pytest.raises(ValueError):
        manifest_checksum(
            "manifest-20260613",
            [{"invoice_id": "inv-1042", "amount": 11901}],
        )

    assert manifest_checksum("manifest-20260613", list(original_rows)) == expected


def test_different_manifest_id_can_bind_changed_payload():
    clear_manifest_checksum_cache()
    original_rows = [{"invoice_id": "inv-1042", "amount": 11900}]
    changed_rows = [{"invoice_id": "inv-1042", "amount": 11901}]

    original_checksum = manifest_checksum("manifest-20260613", original_rows)
    changed_checksum = manifest_checksum("manifest-20260614", changed_rows)

    assert changed_checksum != original_checksum


def test_clear_cache_allows_rebinding_manifest_id():
    clear_manifest_checksum_cache()
    original_rows = [{"invoice_id": "inv-1042", "amount": 11900}]
    changed_rows = [{"invoice_id": "inv-1042", "amount": 11901}]
    manifest_checksum("manifest-20260613", original_rows)

    clear_manifest_checksum_cache()

    assert manifest_checksum("manifest-20260613", changed_rows) == manifest_checksum(
        "manifest-20260613", changed_rows
    )


def test_non_json_payload_preserves_serializer_error():
    clear_manifest_checksum_cache()

    with pytest.raises(TypeError, match="not JSON serializable"):
        manifest_checksum("manifest-20260613", [{"invalid": object()}])
