# Release checkpoint store

TC1 persists release-stream checkpoints in `checkpoint_state`. During the
package 2.9/3.0 overlap window it also maintains the legacy `checkpoints` table.
A checkpoint is ordered by generation and then offset, allowing a new generation
to start again at a smaller offset.

Updates are applied as an atomic batch under an immediate SQLite transaction.
Both layouts and the batch binding commit together. Batch identifiers bind to
updates sorted by stream ID, so reconstruction order is not observable. An
identical retry returns its recorded result; conflicting reuse fails without
modifying either checkpoint layout or the original binding.

Initialization is also one immediate transaction. It creates missing current,
legacy, batch, and metadata tables; reconciles every stream to the greater
`(generation, offset)` found in either layout; canonicalizes safely recoverable
pre-migration batch bindings; and only then publishes the current layout marker.
For an older binding whose result differs from its requested payload, the stored
result's stream order is retained as a verification hint. The first matching
retry can then prove and promote that binding to canonical order without
weakening conflicting-reuse detection. A failed initialization rolls back
completely and may be retried.

During normal overlap, package 3.0 owns writes and package 2.9 reads the legacy
view. On rollback, package 3.0 stops and package 2.9 may advance legacy rows. The
current tables remain in place because old code ignores them. Before package 3.0
accepts another batch, initialization runs again and promotes the greatest value
per stream into both layouts. This supports rollback and later re-entry without
destructive table oscillation.
