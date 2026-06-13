from src.escalation_deadlines import normalize_escalation_deadline


def test_normalizes_offset_deadline_to_utc():
    assert normalize_escalation_deadline("2026-06-17T09:00:00-04:00") == "2026-06-17T13:00:00Z"
