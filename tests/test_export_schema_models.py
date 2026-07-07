from dataclasses import FrozenInstanceError

import pytest

from src.export_schema_models import SchemaSnapshot


def test_snapshot_identity_includes_workspace_and_version():
    first = SchemaSnapshot("ws-204", 7, ("invoice_id",))
    second = SchemaSnapshot("ws-204", 8, ("invoice_id",))

    assert first != second


def test_snapshot_is_immutable():
    snapshot = SchemaSnapshot("ws-204", 7, ("invoice_id",))

    with pytest.raises(FrozenInstanceError):
        snapshot.workspace_version = 8
