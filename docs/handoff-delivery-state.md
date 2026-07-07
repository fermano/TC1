# Handoff delivery retry state

TC1 identifies a transport delivery by producer epoch and delivery identifier.
A sender restart advances the epoch, resets its sequence, and may reuse delivery
identifiers. Replaying an identical delivery within one epoch is idempotent;
changing its payload is rejected.

The in-process state exposes active handoff records in insertion order. Upserts
replace older active values for a signal, and retractions remove active values.
