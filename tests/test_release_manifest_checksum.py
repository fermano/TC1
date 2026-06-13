from src.release_manifest_checksum import (
    clear_manifest_checksum_cache,
    manifest_checksum,
)


def test_identical_retry_payload_reuses_checksum():
    clear_manifest_checksum_cache()
    rows = [{"invoice_id": "inv-1042", "amount": 11900}]

    first = manifest_checksum("manifest-20260613", rows)
    second = manifest_checksum("manifest-20260613", list(rows))

    assert second == first
