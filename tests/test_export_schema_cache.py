from src.export_schema_cache import ExportSchemaCache


def test_reuses_snapshot_for_unchanged_workspace_version():
    cache = ExportSchemaCache()

    first = cache.snapshot("ws-204", 7, ["invoice_id", "amount"])
    second = cache.snapshot("ws-204", 7, ["invoice_id", "amount"])

    assert second is first


def test_replaces_snapshot_when_workspace_version_changes():
    cache = ExportSchemaCache()

    old = cache.snapshot("ws-204", 7, ["invoice_id", "amount"])
    new = cache.snapshot("ws-204", 8, ["invoice_id", "amount", "currency"])

    assert new is not old
    assert new.fields == ("invoice_id", "amount", "currency")


def test_clear_discards_current_snapshot():
    cache = ExportSchemaCache()
    first = cache.snapshot("ws-204", 7, ["invoice_id", "amount"])

    cache.clear()

    second = cache.snapshot("ws-204", 7, ["invoice_id", "amount"])
    assert second == first
    assert second is not first
