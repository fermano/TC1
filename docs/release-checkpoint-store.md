# Release checkpoint store

TC1 persists release-stream checkpoints in `checkpoint_state`. A checkpoint is
ordered by generation and then offset, allowing a new generation to start again
at a smaller offset.

Updates are applied as an atomic batch under an immediate SQLite transaction.
Batch identifiers bind to the canonical ordered update payload. An identical
retry returns its recorded result; conflicting reuse fails without modifying
checkpoint state.
