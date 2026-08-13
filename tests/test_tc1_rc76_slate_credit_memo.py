from src.tc1_rc76_slate_credit_memo import memo_export_row


def test_positive_credit_uses_outlet_scoped_row_key():
    row = memo_export_row(
        {
            "tenant_id": "slate",
            "outlet_id": "web",
            "invoice_id": "inv-314",
            "credit_memo_id": "cm-positive",
            "credit_cents": 125,
        }
    )

    assert row == {
        "row_key": "slate:web:inv-314",
        "action": "credit_memo",
        "source": "rc76-outlet-scoped",
    }


def test_blank_credit_memo_stays_non_credit_default():
    row = memo_export_row(
        {
            "tenant_id": "slate",
            "outlet_id": "retail",
            "invoice_id": "inv-314",
            "credit_memo_id": "",
            "credit_cents": "",
        }
    )

    assert row == {
        "row_key": "slate:retail:inv-314",
        "action": "none",
        "source": "rc76-outlet-scoped",
    }


def test_legacy_outlet_identity_is_preserved():
    row = memo_export_row(
        {
            "tenant_id": "slate",
            "legacy_outlet_id": "partner-portal",
            "legacy_invoice_id": "legacy-881",
            "credit_cents": 49,
        }
    )

    assert row["row_key"] == "slate:partner-portal:legacy-881"
    assert row["action"] == "credit_memo"
