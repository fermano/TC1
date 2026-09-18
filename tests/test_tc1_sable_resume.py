from src.tc1_sable_resume import resume_packets


def test_resume_keeps_one_candidate_packet():
    packets = resume_packets([], [{
        "account_id": "oak",
        "lane_id": "mail",
        "packet_id": "pkt-31",
        "origin": "partner",
        "kind": "schedule",
        "sendAfter": 20,
    }])

    assert packets["oak:mail:pkt-31:partner"]["send_after_seconds"] == 20
    assert packets["oak:mail:pkt-31:partner"]["candidate"] == "sb-5"
    assert packets["oak:mail:pkt-31:partner"]["artifact_ref"] == "sable-rc-5"


def test_sable_packet_keeps_native_and_newer_partner_schedule():
    packets = resume_packets([], [
        {
            "account_id": "oak",
            "lane_id": "mail",
            "packet_id": "pkt-87",
            "origin": "native",
            "kind": "schedule",
            "revision": 3,
            "send_after": 30,
        },
        {
            "account_id": "oak",
            "lane_id": "mail",
            "packet_id": "pkt-87",
            "origin": "",
            "originId": "partner",
            "kind": "schedule",
            "revision": 7,
            "send_after": "",
            "sendAfter": 0,
        },
        {
            "account_id": "oak",
            "lane_id": "mail",
            "packet_id": "pkt-87",
            "origin": "partner",
            "kind": "void",
            "revision": 6,
        },
    ])

    assert sorted(packets) == [
        "oak:mail:pkt-87:native",
        "oak:mail:pkt-87:partner",
    ]
    assert packets["oak:mail:pkt-87:native"] == {
        "state": "queued",
        "send_after_seconds": 30,
        "candidate": "sb-5",
        "lane_signature": "lane:mail",
        "artifact_ref": "sable-rc-5",
        "origin": "native",
    }
    assert packets["oak:mail:pkt-87:partner"] == {
        "state": "queued",
        "send_after_seconds": 0,
        "candidate": "sb-5",
        "lane_signature": "lane:mail",
        "artifact_ref": "sable-rc-5",
        "origin": "partner",
    }


def test_legacy_persisted_packet_key_restarts_as_native_origin():
    assert resume_packets(["oak:mail:pkt-86"], []) == {
        "oak:mail:pkt-86:native": {
            "state": "queued",
            "candidate": "sb-5",
            "lane_signature": "lane:mail",
            "artifact_ref": "sable-rc-5",
            "origin": "native",
        }
    }


def test_newer_void_prevents_older_schedule_from_reappearing():
    packets = resume_packets([], [
        {
            "account_id": "oak",
            "lane_id": "mail",
            "packet_id": "pkt-88",
            "origin": "partner",
            "kind": "void",
            "revision": 8,
        },
        {
            "account_id": "oak",
            "lane_id": "mail",
            "packet_id": "pkt-88",
            "origin": "partner",
            "kind": "schedule",
            "revision": 7,
            "sendAfter": 0,
        },
    ])

    assert packets == {}
