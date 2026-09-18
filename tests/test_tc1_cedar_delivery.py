from src.tc1_cedar_delivery import recipient_decision


def test_active_recipient_with_consent_is_sent():
    assert recipient_decision({"account_state": "active", "delivery_consent": True}) == "send"


def test_active_recipient_without_consent_is_held():
    assert recipient_decision({"account_state": "active"}) == "hold"


def test_closed_recipient_is_skipped():
    assert recipient_decision({"account_state": "closed"}) == "skip"
