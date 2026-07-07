# Release checkpoint rollout

Changes to checkpoint persistence require focused store/model tests, the full
repository suite, repository baseline verification, diff checks, and required
GitHub CI on the proposed head.

Migration and mixed-version fixtures in the repository define the supported
storage boundary. When those fixtures and required checks pass, this TC1 path
does not require a separate production soak or approving review before merge.

Package 2.9 remains supported during the recorded overlap window. Do not delete
or stop updating `checkpoints` until operations confirms all 2.9 partitions are
drained. Package 3.0 initialization is the upgrade and re-entry boundary: it
atomically reconciles legacy/current rows before new batches are accepted.

Rollback is non-destructive. Stop package 3.0 writers and allow 2.9 to continue
using `checkpoints`; leave the current tables present. Re-run package 3.0
initialization before returning to the new worker so rollback advances are
promoted by logical generation/offset. A failed initialization or batch must be
retried only after verifying the transaction left neither layout nor its batch
binding partially committed.
