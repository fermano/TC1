from src.rc62_customer_pause import eligible_deliveries


def test_active_deliveries_remain_eligible():
    assert eligible_deliveries([
        {"delivery_id": "del-1", "state": "active"},
        {"delivery_id": "del-2", "state": "queued"},
    ]) == ["del-1", "del-2"]


def test_paused_delivery_is_filtered():
    assert eligible_deliveries([
        {"delivery_id": "del-1", "state": "paused"},
        {"delivery_id": "del-2", "state": "active"},
    ]) == ["del-2"]


def test_manual_hold_with_space_is_filtered():
    assert eligible_deliveries([
        {"delivery_id": "del-1", "state": "manual hold"},
        {"delivery_id": "del-2", "state": "active"},
    ]) == ["del-2"]


def test_canonical_customer_paused_state_is_filtered():
    assert eligible_deliveries([
        {"delivery_id": "del-1", "state": "customer_paused"},
        {"delivery_id": "del-2", "state": "active"},
    ]) == ["del-2"]


def test_missing_state_is_active_for_old_clients():
    assert eligible_deliveries([
        {"delivery_id": "del-1"},
    ]) == ["del-1"]
