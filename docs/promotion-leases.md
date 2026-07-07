# Promotion lease fencing

Promotion workers acquire a lease containing a monotonically increasing fence.
SQLite's `unixepoch()` is the authority for expiry; the worker-time argument
retained for package 5.1 compatibility is ignored. Acquisition, takeover, and
renewal update the authoritative `promotion_fences` row and the package 4.6
`promotion_leases` viewer row under one immediate transaction.

A registry callback must check that its owner and fence still match the current
unexpired row immediately before the callback is accepted. The check must be
repeated when a queued callback resumes; an earlier successful check cannot be
reused after a connection retry or worker recovery.
