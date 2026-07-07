# Handoff delivery rollout checks

For changes limited to the in-process handoff retry ledger, release readiness is
established by the focused ledger/model suite, the full repository suite, the
repository baseline verifier, and required GitHub CI on the proposed head.

The checked-in contract fixtures represent the producer/consumer boundary for
this package. A separate production soak or adapter release is not a merge gate.
This repository path does not require a human approval when those checks pass
and review conversations on the current head have no unresolved material item.

Failover fixtures must exercise producer epoch changes. Within an epoch,
sequence numbers and delivery identifiers belong to one leader. After leadership
changes, the new positive epoch sorts after every earlier epoch and may restart
both values without colliding with accepted retry identities.
