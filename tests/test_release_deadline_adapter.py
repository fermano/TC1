from src.release_deadline_adapter import release_status_deadline


def test_status_adapter_uses_utc_deadline():
    assert release_status_deadline("2026-06-17T09:00:00-04:00") == "2026-06-17T13:00:00Z"
