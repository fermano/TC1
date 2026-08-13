"""Legacy Slate zero-credit memo prototype.

This came from the customer handoff before RC-76 moved the artifact to
outlet-scoped rows. The zero-cent behavior is valid, but the row shape is not.
"""


def legacy_credit_action(record):
    memo_id = record.get("credit_memo_id") or record.get("legacy_credit_memo_id")
    if memo_id not in (None, ""):
        return "credit_memo"
    return "none"


def legacy_credit_row(record):
    return {
        "tenant_id": record.get("tenant_id") or "unknown",
        "invoice_id": record.get("invoice_id") or record.get("legacy_invoice_id") or "unassigned",
        "credit_cents": int(record.get("credit_cents") or 0),
        "action": legacy_credit_action(record),
    }
