from src.export_schema_cache import clear_export_schema_cache, export_schema


def test_reuses_schema_for_unchanged_workspace_version():
    clear_export_schema_cache()
    fields = ["invoice_id", "amount"]
    first = export_schema("ws-204", 7, fields)
    second = export_schema("ws-204", 7, list(fields))
    assert second == first
