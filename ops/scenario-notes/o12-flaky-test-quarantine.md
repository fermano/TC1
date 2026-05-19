# Flaky test quarantine

Scenario type: flaky test failure
Simulated opened: 2026-05-07
Simulated last activity: 2026-05-14
Expected blocker: unit-tests intermittently fail around timestamp-sensitive release markers
Risk level: medium
Linear tracking: yes

## Change

Documents a quarantine path for the release marker test without proving the root cause.

## Recommended next step

Freeze the clock in tests instead of quarantining the assertion permanently.
