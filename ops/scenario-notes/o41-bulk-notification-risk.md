# Bulk notification risk

Scenario type: notification blast risk
Simulated opened: 2026-05-09
Simulated last activity: 2026-05-14
Expected blocker: rollout can notify every stale PR owner at once
Risk level: high
Linear tracking: yes

## Change

Documents an automation that may create noisy bulk notifications without rate limiting.

## Recommended next step
Add batching and dry-run output before enabling the workflow.
