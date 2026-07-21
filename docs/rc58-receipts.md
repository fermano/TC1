# RC-58 receipt reconciliation

The delivery receipt ledger is consulted after retry and coordinator failover.
Receipt identity is the `(tenant_id, destination_id, event_id)` delivery route,
while attempt ordering within that route prevents an older callback from
replacing newer state.

The supported release window includes databases created before route-aware
receipt tracking. Opening one of those stores migrates its existing rows in a
single transaction and assigns `webhook-primary` as their historical
destination. Stores that already contain destination values retain them while
their primary key is upgraded to the full route. Repository validation must
cover fresh, pre-route, and route-aware SQLite stores.
