# Export schema snapshots

TC1 keeps one immutable `SchemaSnapshot` per workspace. Repeated observations
reuse the snapshot only when the numeric workspace version and complete ordered
field list both match. A version or field-list change replaces the current entry
rather than accumulating workspace history in the process. This matters because
rollback and template-reapply flows can reuse a numeric version for a corrected
field list; the most recently observed complete configuration is current.

New integrations should depend on an `ExportSchemaCache` instance and consume
the snapshot's `fields` tuple. Cache state is intentionally process-local.

The separately deployed invoice scheduler still imports the module-level
`export_schema(workspace_id, workspace_version, fields)` function. That
compatibility helper returns the current snapshot's immutable `fields` tuple and
delegates to the same module-level `ExportSchemaCache` instance; it does not keep
a parallel revision-keyed cache. `clear_export_schema_cache()` clears that shared
state for both call forms.
