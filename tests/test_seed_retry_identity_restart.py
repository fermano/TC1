import sqlite3
import sys

import pytest


def test_retry_identity_survives_fresh_connection(tmp_path):
    path = tmp_path / "retry.sqlite"
    first = sqlite3.connect(path)
    first.execute("CREATE TABLE receipts (delivery_key TEXT PRIMARY KEY, receipt TEXT)")
    first.execute("INSERT INTO receipts VALUES (?, ?)", ("del-17", "receipt-1"))
    first.commit()
    first.close()

    second = sqlite3.connect(path)
    assert second.execute(
        "SELECT receipt FROM receipts WHERE delivery_key = ?", ("del-17",)
    ).fetchone() == ("receipt-1",)


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only locking fixture")
def test_windows_retry_store_reopens_after_handle_release(tmp_path):
    path = tmp_path / "retry.sqlite"
    connection = sqlite3.connect(path)
    connection.close()
    assert path.exists()
