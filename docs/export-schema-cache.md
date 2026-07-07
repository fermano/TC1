# Export schema cache

The export helper accepts a workspace identifier, a numeric workspace version, and
the configured field sequence. Callers receive an immutable tuple of field names.

Entries are reused for an identical workspace/version pair. A changed version
builds a separate entry. The module-level helper remains available to existing
scheduler and invoice-export integrations.
