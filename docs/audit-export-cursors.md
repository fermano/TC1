# Audit export cursors

Audit export cursors are opaque to API consumers, but deployed reconciliation jobs persist the returned string and may resume after a worker restart or rollback.

The current production form is a decimal timestamp. Cursor changes must continue to accept that form for one release window. Ordering must remain deterministic when records are retried or inserted while an export is in progress.
