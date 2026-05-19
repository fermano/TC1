# Backfill idempotency risk

Scenario type: migration idempotency risk
Simulated opened: 2026-05-16
Simulated last activity: 2026-05-19
Expected blocker: backfill may not be safe to rerun
Risk level: critical
Linear tracking: yes

## Change

Adds a backfill plan without idempotency proof or duplicate-run handling.

## Recommended next step
Prove rerun safety and add rollback criteria before approval.
