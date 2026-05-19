# Test fixture brittleness

Scenario type: test fixture brittleness
Simulated opened: 2026-05-13
Simulated last activity: 2026-05-18
Expected blocker: tests depend on exact wall-clock output
Risk level: medium
Linear tracking: yes

## Change

Adds validation guidance that may become flaky when run near minute boundaries.

## Recommended next step

Inject a deterministic clock in tests and avoid asserting raw timestamps.
