"""Benchmark seed: deterministic audit event IDs.

The implementation is intentionally incomplete; cross-region collision coverage is not included.
"""

def audit_event_id(region: str, sequence: int) -> str:
    return f"{region}:{sequence}"
