from src.credit_memo_canary import reconciliation_canary_is_healthy


def test_accepts_clean_reconciliation_samples():
    samples = [{"duplicate": False, "latency_ms": 720}, {"duplicate": False, "latency_ms": 910}]
    assert reconciliation_canary_is_healthy(samples) is True


def test_rejects_duplicate_output():
    assert reconciliation_canary_is_healthy([{"duplicate": True, "latency_ms": 500}]) is False
