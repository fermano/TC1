# Replay claim recovery

Replay claims are stored in the service SQLite database so that restarts do not
erase ownership records. A claim may be retried after its lease expires.

The supported rolling-deploy window includes 4.8 workers reading a database
written by the next patch release. Those workers select named columns from
`replay_claims`; additive columns are tolerated. Removing or changing the
meaning of existing columns is not part of the patch window.

The delivery gateway accepts an optional `idempotency_key` argument. Keys are
opaque to the gateway. Reusing one key suppresses a repeated external delivery,
but different keys are treated as separate attempts.

`ReplayDispatcher` derives that key from the logical replay identity, not from
worker ownership or lease state. The format is
`replay:<stream-length>:<stream>:<cursor>`; the length prefix keeps stream and
cursor boundaries unambiguous. A retry or replacement worker therefore reuses
the same key even when it owns a new claim.

Claim completion remains after the gateway call. If a worker stops after the
gateway accepts a delivery but before completion is recorded, a replacement can
retry without creating a second external delivery during the gateway's
idempotency window. Workers from 4.8 can still read the unchanged claim schema,
but those older dispatchers do not send the stable key. Mixed-version promotion
must account for that limitation separately.

The command-line replay tool and the background replay worker both use
`ReplayDispatcher`.
