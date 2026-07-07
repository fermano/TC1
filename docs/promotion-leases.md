# Promotion leases

Promotion workers coordinate through the `promotion_leases` table. A row records
the resource, owner, and expiry timestamp consumed by the existing operations
viewer. A different owner may replace an expired row.
