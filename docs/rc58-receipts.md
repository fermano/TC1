# RC-58 receipt reconciliation

The delivery receipt ledger is consulted after retry and coordinator failover.
Receipt identity is scoped by the delivery route, while attempt ordering prevents
an older callback from replacing newer state.

The supported release window includes databases created before route-aware
receipt tracking. Repository validation must cover both fresh and existing
SQLite stores.
