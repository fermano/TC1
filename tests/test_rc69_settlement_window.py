from src.rc69_settlement_window import (
    is_release_candidate_manifest,
    manifest_identity,
    settlement_rows,
)


def test_selects_posted_settlement_rows():
    events = [
        {
            "tenant_id": "delta",
            "settlement_id": "st-101",
            "package_type": "settlement",
            "state": "posted",
            "amount_cents": "4200",
        },
        {
            "tenant_id": "delta",
            "settlement_id": "st-102",
            "package_type": "settlement",
            "state": "draft",
            "amount_cents": "1300",
        },
    ]

    assert settlement_rows(events) == [
        {
            "tenant_id": "delta",
            "settlement_id": "st-101",
            "package_type": "settlement",
            "amount_cents": 4200,
        }
    ]


def test_accepts_staging_status_aliases_seen_during_rc69_readout():
    events = [
        {
            "tenant_id": "delta",
            "settlement_id": "st-145",
            "package_type": "settlement",
            "state": "settled-final",
            "amount_cents": 7100,
        },
        {
            "tenant_id": "delta",
            "settlement_id": "st-preview-9",
            "package_type": "settlement",
            "state": "preview-settled",
            "amount_cents": 7100,
        },
    ]

    assert settlement_rows(events) == [
        {
            "tenant_id": "delta",
            "settlement_id": "st-145",
            "package_type": "settlement",
            "amount_cents": 7100,
        },
        {
            "tenant_id": "delta",
            "settlement_id": "st-preview-9",
            "package_type": "settlement",
            "amount_cents": 7100,
        },
    ]


def test_deduplicates_settlement_rows_by_tenant_settlement_and_type():
    events = [
        {
            "tenant_id": "nova",
            "settlement_id": "st-201",
            "package_type": "adjustment",
            "state": "settled",
            "amount_cents": 500,
        },
        {
            "tenant_id": "nova",
            "settlement_id": "st-201",
            "package_type": "adjustment",
            "state": "posted",
            "amount_cents": 900,
        },
    ]

    assert settlement_rows(events) == [
        {
            "tenant_id": "nova",
            "settlement_id": "st-201",
            "package_type": "adjustment",
            "amount_cents": 500,
        }
    ]


def test_manifest_identity_accepts_current_release_ref():
    manifest = {
        "artifact_id": "rc69-settle-west-20260812-b",
        "source_ref": "release/rc-69",
        "source_sha": "9efeed1",
        "package_kind": "settlement",
    }

    assert manifest_identity(manifest) == {
        "artifact_id": "rc69-settle-west-20260812-b",
        "source_ref": "release/rc-69",
        "source_sha": "9efeed1",
        "package_kind": "settlement",
    }
    assert is_release_candidate_manifest(manifest)


def test_manifest_identity_rejects_preview_source_ref():
    manifest = {
        "artifact_id": "rc69-settle-west-20260812-c",
        "source_ref": "release/rc-69-preview",
        "source_sha": "7a1bad0",
        "package_kind": "settlement",
    }

    assert not is_release_candidate_manifest(manifest)
