"""Invoice package manifest helpers for the RC-70 release readout."""

READY_STATES = {"ready", "posted"}
PACKAGE_TYPES = {"invoice", "credit"}


def _normalize(value):
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def invoice_rows(events):
    """Return invoice package rows in stable first-seen order."""
    rows = []
    seen = set()

    for event in events:
        state = _normalize(event.get("state"))
        if state not in READY_STATES:
            continue

        package_type = _normalize(event.get("package_type"))
        if package_type not in PACKAGE_TYPES:
            continue

        key = (event.get("tenant_id"), event.get("invoice_id"), package_type)
        if key in seen:
            continue
        seen.add(key)

        rows.append(
            {
                "tenant_id": event.get("tenant_id"),
                "invoice_id": event.get("invoice_id"),
                "package_type": package_type,
                "amount_cents": int(event.get("amount_cents") or 0),
            }
        )

    return rows


def manifest_identity(manifest):
    """Return stable identity fields used by release-readout checks."""
    return {
        "artifact_id": manifest.get("artifact_id"),
        "source_ref": manifest.get("source_ref") or manifest.get("branch"),
        "source_sha": manifest.get("source_sha") or manifest.get("commit_sha"),
        "package_kind": _normalize(manifest.get("package_kind")),
        "row_count": int(manifest.get("row_count") or 0),
        "expected_row_count": int(manifest.get("expected_row_count") or 0),
        "checksum": manifest.get("checksum"),
        "expected_checksum": manifest.get("expected_checksum"),
    }


def is_promotable_invoice_manifest(manifest, expected_ref="release/rc-70"):
    identity = manifest_identity(manifest)
    checksum_ok = not identity["expected_checksum"] or identity["checksum"] == identity["expected_checksum"]

    return (
        identity["source_ref"] == expected_ref
        and identity["package_kind"] == "invoice"
        and bool(identity["source_sha"])
        and identity["row_count"] == identity["expected_row_count"]
        and checksum_ok
    )
