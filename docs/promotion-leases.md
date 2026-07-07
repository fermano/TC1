# Promotion lease journal

Lease changes are appended to `promotion_lease_events`. A restarted worker
reconstructs current ownership from the highest event sequence for each release
resource. Acquire and release history remains available for diagnosis.
