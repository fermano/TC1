# Export schema snapshots

TC1 keeps one immutable `SchemaSnapshot` per workspace. Repeated reads at the
same workspace version reuse that snapshot. Any observed version change replaces
the current entry rather than accumulating workspace history in the process.

New integrations should depend on an `ExportSchemaCache` instance and consume
the snapshot's `fields` tuple. Cache state is intentionally process-local.
