from src.current_settlement_export import current_settlement_reference
from src.settlement_event_view import structured_settlement_event


def test_structured_committed_settlement_is_current_reference():
    metadata = {
        "settlement": {"token": "vs-120", "state": "committed", "replaces": "vs-118"}
    }

    assert structured_settlement_event(metadata).token == "vs-120"
    assert current_settlement_reference(metadata) == "vs-120"


def test_malformed_or_non_committed_structured_settlement_has_no_current_reference():
    assert current_settlement_reference({"settlement": {"token": "vs-120", "state": "prepared"}}) is None
    assert current_settlement_reference({"settlement": "not-an-event"}) is None
