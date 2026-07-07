from src.export_schema_cache import clear_export_schema_cache, export_schema


def test_reuses_schema_for_unchanged_workspace_version():
    clear_export_schema_cache()
    fields = ["invoice_id", "amount"]
    first = export_schema("ws-204", 7, fields)
    second = export_schema("ws-204", 7, list(fields))
    assert second == first


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
