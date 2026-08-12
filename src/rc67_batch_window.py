"""Batch-window selection for RC-67 partner receipts.

The release job uses this helper to decide which receipt rows belong in a
partner-facing package window.
"""

FINAL_STATES = {"sent", "settled"}


def _normalize(value):
    return str(value or "").strip().lower().replace(" ", "_")


def build_window_rows(receipts, *, window_start, window_end):
    """Return receipt rows whose visible timestamp belongs to the package window."""
    rows = []
    seen = set()

    for receipt in receipts:
        state = _normalize(receipt.get("state"))
        if state not in FINAL_STATES:
            continue

        created_at = receipt.get("created_at")
        if created_at is None or created_at < window_start or created_at >= window_end:
            continue

        key = (receipt.get("tenant_id"), receipt.get("receipt_id"))
        if key in seen:
            continue
        seen.add(key)

        rows.append(
            {
                "tenant_id": receipt.get("tenant_id"),
                "receipt_id": receipt.get("receipt_id"),
                "amount_cents": receipt.get("amount_cents", 0),
                "created_at": created_at,
            }
        )

    return rows
