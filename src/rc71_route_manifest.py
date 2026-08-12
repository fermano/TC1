"""Route-scoped invoice manifest helpers for RC-71."""

EXPORTABLE_STATES = {"ready", "posted"}
RETRACT_STATES = {"voided", "retracted", "cancelled", "canceled"}


def _normalize(value):
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def _route_id(event):
    return event.get("route_id") or event.get("partner_id") or "primary"


def _sequence(event):
    try:
        return int(event.get("sequence") or event.get("event_sequence") or 0)
    except (TypeError, ValueError):
        return 0


def manifest_rows(events):
    """Return exportable invoice rows in first-seen order."""
    rows_by_invoice = {}
    order = []

    for event in events:
        tenant_id = event.get("tenant_id")
        invoice_id = event.get("invoice_id")
        if not tenant_id or not invoice_id:
            continue

        state = _normalize(event.get("state"))
        if state not in EXPORTABLE_STATES | RETRACT_STATES:
            continue

        key = (tenant_id, invoice_id)
        event_sequence = _sequence(event)
        current = rows_by_invoice.get(key)
        if current and current["sequence"] > event_sequence:
            continue

        if key not in rows_by_invoice:
            order.append(key)

        if state in RETRACT_STATES:
            rows_by_invoice[key] = {
                "tenant_id": tenant_id,
                "invoice_id": invoice_id,
                "route_id": _route_id(event),
                "state": state,
                "sequence": event_sequence,
                "amount_cents": int(event.get("amount_cents") or 0),
                "_retracted": True,
            }
            continue

        rows_by_invoice[key] = {
            "tenant_id": tenant_id,
            "invoice_id": invoice_id,
            "route_id": _route_id(event),
            "state": state,
            "sequence": event_sequence,
            "amount_cents": int(event.get("amount_cents") or 0),
            "_retracted": False,
        }

    return [
        {key: value for key, value in rows_by_invoice[invoice_key].items() if key != "_retracted"}
        for invoice_key in order
        if invoice_key in rows_by_invoice and not rows_by_invoice[invoice_key].get("_retracted")
    ]


def manifest_identity(manifest):
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


def is_promotable_route_manifest(manifest, expected_ref="release/rc-71"):
    identity = manifest_identity(manifest)
    checksum_ok = not identity["expected_checksum"] or identity["checksum"] == identity["expected_checksum"]
    return (
        identity["source_ref"] == expected_ref
        and identity["package_kind"] == "route_invoice"
        and bool(identity["source_sha"])
        and identity["row_count"] == identity["expected_row_count"]
        and checksum_ok
    )
