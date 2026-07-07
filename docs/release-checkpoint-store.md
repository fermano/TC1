# Release checkpoint migration

The checkpoint schema may be upgraded from the legacy `checkpoints` table to
`checkpoint_state`. Rollback copies current values back to the legacy table
before removing the new table. A later upgrade repeats the copy.

This permits the release package to return to the previous storage layout during
the rollback window.
