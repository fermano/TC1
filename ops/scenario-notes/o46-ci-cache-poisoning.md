# CI cache poisoning suspicion

Scenario type: CI cache poisoning suspicion
Simulated opened: 2026-05-12
Simulated last activity: 2026-05-17
Expected blocker: passing CI may be using stale cached fixture data
Risk level: high
Linear tracking: yes

## Change

Captures a scenario where green checks are not trusted because cache invalidation is unclear.

## Recommended next step
Clear cache and rerun CI before approval.
