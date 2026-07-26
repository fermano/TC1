from src.batch_failure_context import batch_failure_context


def test_successful_batch_has_no_failure_context():
    assert batch_failure_context([{"ok": True}, {"ok": True}]) is None


def test_failed_batch_exposes_error_context():
    assert batch_failure_context([
        {"ok": True},
        {"ok": False, "error": "gateway timeout"},
    ]) == "gateway timeout"
