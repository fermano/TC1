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
    assert packets["oak:mail:pkt-31:partner"]["candidate"] == "sb-4"


def test_partner_origin_alias_does_not_replace_native_packet():
    packets = resume_packets([], [
        {
            "account_id": "oak", "lane_id": "mail", "packet_id": "pkt-33",
            "origin": "native", "kind": "schedule", "send_after": 40,
        },
        {
            "account_id": "oak", "lane_id": "mail", "packet_id": "pkt-33",
            "origin": "", "originId": "partner", "kind": "schedule", "sendAfter": 0,
        },
    ])
    assert packets["oak:mail:pkt-33:native"]["send_after_seconds"] == 40
    assert packets["oak:mail:pkt-33:partner"]["send_after_seconds"] == 0
