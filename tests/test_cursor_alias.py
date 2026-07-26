from src.cursor_alias import select_cursor


def test_reads_legacy_alias():
    assert select_cursor({"after": "page-17"}) == "page-17"


def test_reads_canonical_cursor():
    assert select_cursor({"cursor": "page-18"}) == "page-18"
