from src.rc70_invoice_manifest import invoice_rows, is_promotable_invoice_manifest, manifest_identity


def test_invoice_rows_keep_first_ready_package_by_invoice_and_type():
    events = [
        {"tenant_id": "atlas", "invoice_id": "inv-101", "package_type": "invoice", "state": "draft", "amount_cents": 2300},
        {"tenant_id": "atlas", "invoice_id": "inv-101", "package_type": "invoice", "state": "ready", "amount_cents": 2300},
        {"tenant_id": "atlas", "invoice_id": "inv-101", "package_type": "invoice", "state": "posted", "amount_cents": 2400},
        {"tenant_id": "atlas", "invoice_id": "cr-101", "package_type": "credit", "state": "ready", "amount_cents": -600},
        {"tenant_id": "atlas", "invoice_id": "memo-101", "package_type": "memo", "state": "ready", "amount_cents": 200},
    ]

    assert invoice_rows(events) == [
        {"tenant_id": "atlas", "invoice_id": "inv-101", "package_type": "invoice", "amount_cents": 2300},
        {"tenant_id": "atlas", "invoice_id": "cr-101", "package_type": "credit", "amount_cents": -600},
    ]


def test_invoice_manifest_requires_release_branch_identity_and_matching_counts():
    manifest = {
        "artifact_id": "rc70-invoice-east-20260812-g",
        "source_ref": "release/rc-70",
        "source_sha": "abc1234",
        "package_kind": "invoice",
        "row_count": 260,
        "expected_row_count": 260,
        "checksum": "8c41e7b",
        "expected_checksum": "8c41e7b",
    }

    assert is_promotable_invoice_manifest(manifest)

    stale_manifest = {**manifest, "source_ref": "release/rc-70-shadow"}
    assert not is_promotable_invoice_manifest(stale_manifest)


def test_manifest_identity_accepts_legacy_key_names():
    identity = manifest_identity(
        {
            "artifact_id": "rc70-invoice-east-20260812-f",
            "branch": "release/rc-70",
            "commit_sha": "def5678",
            "package_kind": "Invoice",
            "row_count": "260",
            "expected_row_count": "260",
        }
    )

    assert identity["source_ref"] == "release/rc-70"
    assert identity["source_sha"] == "def5678"
    assert identity["package_kind"] == "invoice"
    assert identity["row_count"] == 260
