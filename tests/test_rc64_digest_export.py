from src.rc64_digest_export import build_digest_candidates


def test_skips_suppressed_rows_and_unsupported_channels():
    rows = [
        {
            "tenant_id": "t1",
            "contact_id": "c1",
            "channel": "email",
            "state": "suppressed",
            "address": "c1@example.test",
        },
        {
            "tenant_id": "t1",
            "contact_id": "c2",
            "channel": "push",
            "state": "active",
            "address": "device-2",
        },
        {
            "tenant_id": "t1",
            "contact_id": "c3",
            "channel": "sms",
            "state": "active",
            "address": "+15550000003",
        },
    ]

    assert build_digest_candidates(rows) == [
        {
            "tenant_id": "t1",
            "contact_id": "c3",
            "channel": "sms",
            "address": "+15550000003",
        }
    ]


def test_deduplicates_by_tenant_contact_and_channel():
    rows = [
        {
            "tenant_id": "t1",
            "contact_id": "c1",
            "channel": "Email",
            "state": "active",
            "address": "first@example.test",
        },
        {
            "tenant_id": "t1",
            "contact_id": "c1",
            "channel": "email",
            "state": "active",
            "address": "second@example.test",
        },
        {
            "tenant_id": "t1",
            "contact_id": "c1",
            "channel": "sms",
            "state": "active",
            "address": "+15550000001",
        },
    ]

    assert build_digest_candidates(rows) == [
        {
            "tenant_id": "t1",
            "contact_id": "c1",
            "channel": "email",
            "address": "first@example.test",
        },
        {
            "tenant_id": "t1",
            "contact_id": "c1",
            "channel": "sms",
            "address": "+15550000001",
        },
    ]


def test_skips_boolean_retired_contact_rows():
    rows = [
        {
            "tenant_id": "west",
            "contact_id": "c-retired",
            "channel": "email",
            "state": "active",
            "retired": True,
            "address": "retired@example.test",
        },
        {
            "tenant_id": "west",
            "contact_id": "c-active",
            "channel": "email",
            "state": "active",
            "retired": False,
            "address": "active@example.test",
        },
    ]

    assert build_digest_candidates(rows) == [
        {
            "tenant_id": "west",
            "contact_id": "c-active",
            "channel": "email",
            "address": "active@example.test",
        }
    ]


def test_skips_contacts_with_retired_timestamp_from_archive_replay():
    rows = [
        {
            "tenant_id": "west",
            "contact_id": "cnt-8841",
            "channel": "email",
            "state": "active",
            "retired": False,
            "retired_at": "2026-08-11T18:42:13Z",
            "address": "retired-west@example.test",
        },
        {
            "tenant_id": "west",
            "contact_id": "cnt-active",
            "channel": "email",
            "state": "active",
            "retired": False,
            "retired_at": "",
            "address": "active-west@example.test",
        },
        {
            "tenant_id": "west",
            "contact_id": "cnt-no-retirement",
            "channel": "sms",
            "state": "active",
            "retired": False,
            "address": "+15550008841",
        },
    ]

    assert build_digest_candidates(rows) == [
        {
            "tenant_id": "west",
            "contact_id": "cnt-active",
            "channel": "email",
            "address": "active-west@example.test",
        },
        {
            "tenant_id": "west",
            "contact_id": "cnt-no-retirement",
            "channel": "sms",
            "address": "+15550008841",
        },
    ]
