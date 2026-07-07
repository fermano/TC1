# Handoff delivery ledger

TC1 keeps an in-process ledger for transport retries. Delivery identifiers bind
to their first accepted event. Replaying that event is idempotent; a conflicting
reuse is rejected.

Each logical signal retains its highest observed sequence even while inactive.
Retractions therefore leave a tombstone, preventing an older upsert from
resurrecting a cleared signal. A later sequence can reactivate the signal without
moving its first-seen dashboard position.
