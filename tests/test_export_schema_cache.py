from src.export_schema_cache import (
    ExportSchemaCache,
    clear_export_schema_cache,
    export_schema,
    export_schema_cache,
)


def test_reuses_snapshot_for_unchanged_workspace_version():
    cache = ExportSchemaCache()

    first = cache.snapshot("ws-204", 7, ["invoice_id", "amount"])
    second = cache.snapshot(
        "ws-204", 7, (field for field in ["invoice_id", "amount"])
    )

    assert second is first


def test_replaces_snapshot_when_workspace_version_changes():
    cache = ExportSchemaCache()

    old = cache.snapshot("ws-204", 7, ["invoice_id", "amount"])
    new = cache.snapshot("ws-204", 8, ["invoice_id", "amount", "currency"])

    assert new is not old
    assert new.fields == ("invoice_id", "amount", "currency")


def test_replaces_snapshot_when_fields_change_at_same_version():
    cache = ExportSchemaCache()

    current = cache.snapshot("ws-204", 42, ["invoice_id", "amount", "tax_code"])
    corrected = cache.snapshot("ws-204", 42, ["invoice_id", "amount"])

    assert corrected is not current
    assert corrected.workspace_version == 42
    assert corrected.fields == ("invoice_id", "amount")


def test_replaces_arbor_snapshot_after_partner_revision_rollback():
    cache = ExportSchemaCache()

    current = cache.snapshot(
        "arbor-41", 18, ["invoice_id", "amount", "tax_code"]
    )
    rolled_back = cache.snapshot("arbor-41", 17, ["invoice_id", "amount"])

    assert rolled_back is not current
    assert rolled_back.workspace_version == 17
    assert rolled_back.fields == ("invoice_id", "amount")


def test_arbor_rollback_does_not_clear_unrelated_workspace_snapshot():
    cache = ExportSchemaCache()

    other = cache.snapshot("cedar-17", 17, ["invoice_id", "tax_code"])
    cache.snapshot("arbor-41", 18, ["invoice_id", "amount", "tax_code"])
    cache.snapshot("arbor-41", 17, ["invoice_id", "amount"])
    repeated_other = cache.snapshot("cedar-17", 17, ["invoice_id", "tax_code"])

    assert repeated_other is other


def test_clear_discards_current_snapshot():
    cache = ExportSchemaCache()
    first = cache.snapshot("ws-204", 7, ["invoice_id", "amount"])

    cache.clear()

    second = cache.snapshot("ws-204", 7, ["invoice_id", "amount"])
    assert second == first
    assert second is not first


def test_builds_new_schema_when_workspace_version_changes():
    clear_export_schema_cache()

    old = export_schema("ws-204", 7, ["invoice_id", "amount"])
    new = export_schema("ws-204", 8, ["invoice_id", "amount", "currency"])

    assert old == ("invoice_id", "amount")
    assert new == ("invoice_id", "amount", "currency")


def test_separates_workspaces_with_the_same_version():
    clear_export_schema_cache()

    first = export_schema("ws-204", 8, ["invoice_id", "currency"])
    second = export_schema("ws-771", 8, ["invoice_id", "tax_code"])

    assert first != second


def test_legacy_helper_uses_module_snapshot_cache_and_returns_tuple():
    clear_export_schema_cache()

    fields = export_schema("ws-204", 7, ["invoice_id", "amount"])
    snapshot = export_schema_cache.snapshot(
        "ws-204", 7, ["invoice_id", "amount"]
    )

    assert fields == ("invoice_id", "amount")
    assert fields is snapshot.fields


def test_clear_discards_legacy_helper_snapshot():
    clear_export_schema_cache()
    first = export_schema("ws-204", 7, ["invoice_id", "amount"])

    clear_export_schema_cache()

    second = export_schema("ws-204", 7, ["invoice_id", "amount"])
    assert second == first
    assert second is not first
