from src.rc61_release_gate import evaluate_release_checks


def test_release_gate_is_ready_when_required_checks_pass():
    decision = evaluate_release_checks([
        {"name": "unit", "state": "passed", "required": True},
        {"name": "preview", "state": "skipped", "required": True},
    ])

    assert decision == {"ready": True, "blockers": [], "advisory": []}


def test_release_gate_blocks_failed_required_check():
    decision = evaluate_release_checks([
        {"name": "artifact", "state": "failed", "required": True},
    ])

    assert decision == {"ready": False, "blockers": ["artifact"], "advisory": []}


def test_release_gate_blocks_manual_hold_with_space():
    decision = evaluate_release_checks([
        {"name": "customer-hold", "state": "manual hold", "required": True},
    ])

    assert decision == {"ready": False, "blockers": ["customer-hold"], "advisory": []}


def test_release_gate_blocks_canonical_manual_hold_state():
    decision = evaluate_release_checks([
        {"name": "customer-hold", "state": "manual_hold", "required": True},
    ])

    assert decision == {"ready": False, "blockers": ["customer-hold"], "advisory": []}


def test_optional_unknown_state_is_advisory_only():
    decision = evaluate_release_checks([
        {"name": "copy-review", "state": "waiting", "required": False},
    ])

    assert decision == {"ready": True, "blockers": [], "advisory": ["copy-review"]}
