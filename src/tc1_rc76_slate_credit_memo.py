"""RC-76 Slate credit memo export helper.

The RC-76 artifact emits outlet-scoped credit memo rows so the same tenant and
invoice can carry different outlet decisions without collapsing identity.
"""


def memo_row_key(record):
    tenant = record.get("tenant_id") or "unknown"
    outlet = record.get("outlet_id") or record.get("legacy_outlet_id") or record.get("destination_id") or "default"
    invoice = record.get("invoice_id") or record.get("legacy_invoice_id") or "unassigned"
    return f"{tenant}:{outlet}:{invoice}"


def memo_action(record):
    cents = record.get("credit_cents") or record.get("adjustment_cents")
    if cents:
        return "credit_memo"
    return "none"


def memo_export_row(record):
    return {
        "row_key": memo_row_key(record),
        "action": memo_action(record),
        "source": "rc76-outlet-scoped",
    }
