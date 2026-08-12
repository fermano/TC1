from src.rc71_route_manifest import manifest_rows, is_promotable_route_manifest, manifest_identity


def test_manifest_rows_emit_latest_ready_invoice_once():
    events = [
        {"tenant_id": "atlas", "invoice_id": "inv-101", "route_id": "card", "state": "draft", "sequence": 1, "amount_cents": 1000},
        {"tenant_id": "atlas", "invoice_id": "inv-101", "route_id": "card", "state": "ready", "sequence": 2, "amount_cents": 1000},
        {"tenant_id": "atlas", "invoice_id": "inv-101", "route_id": "card", "state": "posted", "sequence": 3, "amount_cents": 1100},
    ]

    assert manifest_rows(events) == [
        {
            "tenant_id": "atlas",
            "invoice_id": "inv-101",
            "route_id": "card",
            "state": "posted",
            "sequence": 3,
            "amount_cents": 1100,
        }
    ]


def test_manifest_rows_keep_same_invoice_on_two_current_routes():
    events = [
        {"tenant_id": "atlas", "invoice_id": "inv-771", "route_id": "card", "state": "posted", "sequence": 41, "amount_cents": 1200},
        {"tenant_id": "atlas", "invoice_id": "inv-771", "route_id": "bank", "state": "posted", "sequence": 4, "amount_cents": 1200},
    ]

    assert [row["route_id"] for row in manifest_rows(events)] == ["card", "bank"]


def test_manifest_rows_apply_retractions_per_route():
    events = [
        {"tenant_id": "atlas", "invoice_id": "inv-771", "route_id": "card", "state": "posted", "sequence": 41, "amount_cents": 1200},
        {"tenant_id": "atlas", "invoice_id": "inv-771", "route_id": "card", "state": "voided", "sequence": 42, "amount_cents": 1200},
        {"tenant_id": "atlas", "invoice_id": "inv-771", "route_id": "bank", "state": "posted", "sequence": 4, "amount_cents": 1200},
    ]

    assert manifest_rows(events) == [
        {
            "tenant_id": "atlas",
            "invoice_id": "inv-771",
            "route_id": "bank",
            "state": "posted",
            "sequence": 4,
            "amount_cents": 1200,
        }
    ]


def test_manifest_rows_ignore_older_route_retraction():
    events = [
        {"tenant_id": "atlas", "invoice_id": "inv-772", "route_id": "bank", "state": "voided", "event_sequence": 4, "amount_cents": 1200},
        {"tenant_id": "atlas", "invoice_id": "inv-772", "route_id": "bank", "state": "posted", "event_sequence": 5, "amount_cents": 1200},
    ]

    assert manifest_rows(events) == [
        {
            "tenant_id": "atlas",
            "invoice_id": "inv-772",
            "route_id": "bank",
            "state": "posted",
            "sequence": 5,
            "amount_cents": 1200,
        }
    ]


def test_manifest_rows_accept_legacy_partner_id_route():
    events = [
        {"tenant_id": "atlas", "invoice_id": "inv-102", "partner_id": "bank", "state": "posted", "sequence": "7", "amount_cents": 2500},
    ]

    assert manifest_rows(events)[0]["route_id"] == "bank"
    assert manifest_rows(events)[0]["sequence"] == 7


def test_route_manifest_identity_requires_release_branch():
    manifest = {
        "artifact_id": "rc71-route-invoice-20260812-f",
        "source_ref": "release/rc-71",
        "source_sha": "abc1234",
        "package_kind": "route_invoice",
        "row_count": 118,
        "expected_row_count": 118,
        "checksum": "b9417aa",
        "expected_checksum": "b9417aa",
    }

    assert is_promotable_route_manifest(manifest)
    assert not is_promotable_route_manifest({**manifest, "source_ref": "release/rc-71-preview"})


def test_manifest_identity_accepts_legacy_key_names():
    identity = manifest_identity(
        {
            "artifact_id": "rc71-route-invoice-20260812-e",
            "branch": "release/rc-71",
            "commit_sha": "def5678",
            "package_kind": "Route Invoice",
            "row_count": "118",
            "expected_row_count": "118",
        }
    )

    assert identity["source_ref"] == "release/rc-71"
    assert identity["source_sha"] == "def5678"
    assert identity["package_kind"] == "route_invoice"
    assert identity["row_count"] == 118
