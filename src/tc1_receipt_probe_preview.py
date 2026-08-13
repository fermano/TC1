"""Receipt probe preview helpers for TC1 retry dashboard."""


def preview_receipt_count(rows, *, include_pending=False):
    visible = []
    for row in rows:
        if row.get("receipt_id"):
            visible.append(row)
        elif include_pending and row.get("state") == "pending":
            visible.append(row)
    return len(visible)
