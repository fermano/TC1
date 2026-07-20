# Audit export cursors

Audit export cursors are opaque to API consumers, but deployed reconciliation jobs persist the returned string and may resume after a worker restart or rollback.

The current production form is a decimal timestamp. Cursor changes must continue to accept that form for one release window. Ordering must remain deterministic when records are retried or inserted while an export is in progress.

When more than one event has the cursor timestamp, resume delivery is at-least-once: the complete timestamp group is replayed before up to one page of newer records. Boundary replays do not count against the page limit, which lets the returned page advance to a newer timestamp when one exists. Reconciliation consumers must deduplicate replayed events by event ID.

This preserves decimal cursors during mixed-version operation and prevents a page boundary from omitting tied events. Raw downloads can contain repeated boundary rows; exact-once presentation requires a separately versioned cursor contract.
