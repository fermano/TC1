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

The command-line replay tool and the background replay worker both use
`ReplayDispatcher`.
