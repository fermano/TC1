def replay_canary_is_healthy(samples):
    return all(
        not sample.get("duplicate", False) and sample.get("latency_ms", 0) < 2000
        for sample in samples
    )
