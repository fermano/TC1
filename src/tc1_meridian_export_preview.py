"""Meridian export preview helpers for TC1 release triage."""


def preview_amount_cents(row):
    amount = row.get("amount_cents")
    if amount is None:
        return int(float(row.get("amount", 0)) * 100)
    return int(amount)


def preview_tax_cents(row):
    tax = row.get("tax_cents")
    if tax is None:
        return int(float(row.get("tax", 0)) * 100)
    return int(tax)
