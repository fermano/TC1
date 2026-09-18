from src.tc1_cedar_delivery import recipient_decision


def test_active_recipient_with_consent_is_sent():
    assert recipient_decision({"account_state": "active", "delivery_consent": True}) == "send"


def test_established_active_recipient_without_a_flag_is_sent():
    assert recipient_decision({"account_state": "active"}) == "send"


def test_explicitly_opted_out_recipient_is_held():
    assert recipient_decision({"account_state": "active", "delivery_consent": False}) == "hold"
