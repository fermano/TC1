from src.notification_replay_canary import replay_canary_is_healthy


def test_accepts_clean_replay_samples():
    samples = [
        {"duplicate": False, "latency_ms": 420},
        {"duplicate": False, "latency_ms": 610},
    ]
    assert replay_canary_is_healthy(samples) is True


def test_rejects_duplicate_delivery():
    assert replay_canary_is_healthy([{"duplicate": True, "latency_ms": 300}]) is False
