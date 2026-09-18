from src.tc1_cedar_delivery import recipient_decision


def test_active_recipient_is_sent():
    assert recipient_decision({"account_state": "active"}) == "send"


def test_closed_recipient_is_skipped():
    assert recipient_decision({"account_state": "closed"}) == "skip"
