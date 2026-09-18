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
