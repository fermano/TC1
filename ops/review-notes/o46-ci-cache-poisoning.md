# CI cache poisoning suspicion

First raised: 2026-05-12
Last update: 2026-05-17

Review concern: passing CI may be using stale cached baseline data

## Change

Captures a case where green checks are not trusted because cache invalidation is unclear.

## Recommended next step
Clear cache and rerun CI before approval.
