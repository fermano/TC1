from src.rc66_partner_export import build_partner_export_rows


def test_exports_supported_partner_events_once():
    events = [
        {
            "tenant_id": "pilot",
            "partner": "Atlas",
            "external_id": "ship-1",
            "event_type": "shipment",
            "state": "posted",
            "amount_cents": 4100,
        },
        {
            "tenant_id": "pilot",
            "partner": "atlas",
            "external_id": "ship-1",
            "event_type": "shipment",
            "state": "posted",
            "amount_cents": 4200,
        },
        {
            "tenant_id": "pilot",
            "partner": "nova",
            "external_id": "retry-1",
            "event_type": "retry",
            "state": "ready",
            "amount_cents": 900,
        },
    ]

    assert build_partner_export_rows(events) == [
        {
            "tenant_id": "pilot",
            "partner": "atlas",
            "external_id": "ship-1",
            "event_type": "shipment",
            "amount_cents": 4100,
        },
        {
            "tenant_id": "pilot",
            "partner": "nova",
            "external_id": "retry-1",
            "event_type": "retry",
            "amount_cents": 900,
        },
    ]


def test_skips_dry_run_and_unknown_partner_rows():
    events = [
        {
            "tenant_id": "pilot",
            "partner": "atlas",
            "external_id": "ship-2",
            "event_type": "shipment",
            "state": "posted",
            "amount_cents": 800,
            "dry_run": True,
        },
        {
            "tenant_id": "pilot",
            "partner": "sandbox_partner",
            "external_id": "ship-3",
            "event_type": "shipment",
            "state": "posted",
            "amount_cents": 700,
        },
    ]

    assert build_partner_export_rows(events) == []


def test_skips_unposted_rows():
    events = [
        {
            "tenant_id": "pilot",
            "partner": "atlas",
            "external_id": "ship-4",
            "event_type": "shipment",
            "state": "draft",
            "amount_cents": 500,
        }
    ]

    assert build_partner_export_rows(events) == []
