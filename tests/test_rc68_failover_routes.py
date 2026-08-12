from src.rc68_failover_routes import build_failover_routes


def test_routes_ready_events_by_region():
    events = [
        {
            "tenant_id": "t1",
            "delivery_id": "d1",
            "event_type": "delivery",
            "state": "ready",
            "region": "EU",
        },
        {
            "tenant_id": "t1",
            "delivery_id": "d2",
            "event_type": "preview",
            "state": "ready",
            "region": "us",
        },
        {
            "tenant_id": "t1",
            "delivery_id": "d3",
            "event_type": "retry",
            "state": "draft",
            "region": "apac",
        },
    ]

    assert build_failover_routes(events) == [
        {
            "tenant_id": "t1",
            "delivery_id": "d1",
            "event_type": "delivery",
            "route_region": "eu",
        }
    ]


def test_routes_region_hint_from_release_notes():
    events = [
        {
            "tenant_id": "t6",
            "delivery_id": "d12",
            "event_type": "delivery",
            "state": "ready",
            "region": "",
            "region_hint": "EU",
        }
    ]

    assert build_failover_routes(events) == [
        {
            "tenant_id": "t6",
            "delivery_id": "d12",
            "event_type": "delivery",
            "route_region": "eu",
        }
    ]


def test_unknown_region_uses_global_route():
    events = [
        {
            "tenant_id": "t2",
            "delivery_id": "d4",
            "event_type": "retry",
            "state": "queued",
            "region": "moon",
        }
    ]

    assert build_failover_routes(events) == [
        {
            "tenant_id": "t2",
            "delivery_id": "d4",
            "event_type": "retry",
            "route_region": "global",
        }
    ]


def test_deduplicates_by_tenant_delivery_and_event_type():
    events = [
        {
            "tenant_id": "t3",
            "delivery_id": "d5",
            "event_type": "delivery",
            "state": "ready",
            "region": "us",
        },
        {
            "tenant_id": "t3",
            "delivery_id": "d5",
            "event_type": "delivery",
            "state": "queued",
            "region": "eu",
        },
    ]

    assert build_failover_routes(events) == [
        {
            "tenant_id": "t3",
            "delivery_id": "d5",
            "event_type": "delivery",
            "route_region": "us",
        }
    ]
