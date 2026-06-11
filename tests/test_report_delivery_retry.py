from src.report_delivery_retry import retry_delay


def test_502_honors_retry_after_header() -> None:
    assert retry_delay(502, retry_after=12, attempt=1) == 12
