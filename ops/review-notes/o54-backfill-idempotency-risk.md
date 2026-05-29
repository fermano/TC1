# Backfill idempotency risk

First raised: 2026-05-16
Last update: 2026-05-19

Review concern: backfill may not be safe to rerun

## Change

Adds a backfill plan without idempotency proof or duplicate-run handling.

## Recommended next step
Prove rerun safety and add rollback criteria before approval.
