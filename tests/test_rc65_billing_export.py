from src.rc65_billing_export import build_billing_candidates


def test_skips_non_billable_states_and_unsupported_event_types():
    events = [
        {
            "tenant_id": "north",
            "event_id": "evt-1",
            "event_type": "delivery",
            "state": "refunded",
            "amount_cents": 500,
        },
        {
            "tenant_id": "north",
            "event_id": "evt-2",
            "event_type": "preview",
            "state": "active",
            "amount_cents": 700,
        },
        {
            "tenant_id": "north",
            "event_id": "evt-3",
            "event_type": "retry",
            "state": "active",
            "amount_cents": 900,
        },
    ]

    assert build_billing_candidates(events) == [
        {
            "tenant_id": "north",
            "event_id": "evt-3",
            "event_type": "retry",
            "amount_cents": 900,
        }
    ]


def test_preserves_legacy_rows_without_environment_metadata():
    events = [
        {
            "tenant_id": "legacy",
            "event_id": "evt-4",
            "event_type": "delivery",
            "state": "active",
            "amount_cents": 1100,
        }
    ]

    assert build_billing_candidates(events) == [
        {
            "tenant_id": "legacy",
            "event_id": "evt-4",
            "event_type": "delivery",
            "amount_cents": 1100,
        }
    ]


def test_deduplicates_by_tenant_event_and_type():
    events = [
        {
            "tenant_id": "north",
            "event_id": "evt-5",
            "event_type": "Delivery",
            "state": "active",
            "amount_cents": 1200,
        },
        {
            "tenant_id": "north",
            "event_id": "evt-5",
            "event_type": "delivery",
            "state": "active",
            "amount_cents": 1300,
        },
    ]

    assert build_billing_candidates(events) == [
        {
            "tenant_id": "north",
            "event_id": "evt-5",
            "event_type": "delivery",
            "amount_cents": 1200,
        }
    ]


def test_skips_explicit_test_mode_events():
    events = [
        {
            "tenant_id": "trial",
            "event_id": "evt-6",
            "event_type": "delivery",
            "state": "active",
            "mode": "test_mode",
            "amount_cents": 1500,
        },
        {
            "tenant_id": "trial",
            "event_id": "evt-7",
            "event_type": "delivery",
            "state": "active",
            "mode": "live",
            "amount_cents": 1700,
        },
    ]

    assert build_billing_candidates(events) == [
        {
            "tenant_id": "trial",
            "event_id": "evt-7",
            "event_type": "delivery",
            "amount_cents": 1700,
        }
    ]
