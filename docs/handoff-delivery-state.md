# Handoff delivery ledger

TC1 keeps an in-process ledger for transport retries. Delivery identifiers bind
within one positive producer epoch to their first accepted event. Replaying that
event is idempotent; a conflicting reuse in the same epoch is rejected. When
producer leadership changes, the new epoch may restart both sequence values and
delivery identifiers.

Each logical signal retains its highest observed `(producer_epoch, sequence)`
even while inactive. Retractions therefore leave a tombstone, preventing an
older upsert from resurrecting a cleared signal. Any event in a newer epoch is
later than every event in an older epoch; a later logical version can reactivate
the signal without moving its first-seen dashboard position.
