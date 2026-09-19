import hashlib
import json

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


def test_distinct_ember_platform_tokens_do_not_share_retry_binding():
    clear_manifest_checksum_cache()

    amd64 = manifest_checksum(
        "EMBER-17@linux-amd64",
        [{"artifact": "sha256:7c09", "platform": "linux-amd64"}],
    )
    arm64 = manifest_checksum(
        "ember-17@linux-arm64",
        [{"artifact": "sha256:9d4a", "platform": "linux-arm64"}],
    )

    assert amd64 != arm64


def test_changed_payload_for_same_ember_platform_token_still_raises():
    clear_manifest_checksum_cache()
    manifest_checksum(
        "ember-17@linux-amd64",
        [{"artifact": "sha256:7c09", "platform": "linux-amd64"}],
    )

    with pytest.raises(ValueError, match="already bound"):
        manifest_checksum(
            "EMBER-17@linux-amd64",
            [{"artifact": "sha256:changed", "platform": "linux-amd64"}],
        )


def test_provider_spelling_remains_part_of_retry_identity():
    clear_manifest_checksum_cache()

    underscore = manifest_checksum(
        "ember-17@eu_west",
        [{"provider": "eu_west", "artifact": "sha256:7c09"}],
    )
    hyphen = manifest_checksum(
        "ember-17@eu-west",
        [{"provider": "eu-west", "artifact": "sha256:9d4a"}],
    )

    assert underscore != hyphen


def test_checksum_remains_payload_signature_not_token_scoped():
    clear_manifest_checksum_cache()
    rows = [{"artifact": "sha256:7c09", "platform": "linux-amd64"}]

    assert manifest_checksum("ember-17@linux-amd64", rows) == hashlib.sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


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
