# RC-68 failover routes

Failover packages route ready delivery and retry rows to partner regions.

Most rows carry a top-level `region`. Newer routing experiments may attach a
nested routing context, while older failover replay rows can carry fallback
metadata from the queue adapter.

Release checks should compare the package against the row shape actually present
in the candidate artifact.
