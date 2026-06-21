# Flaky test quarantine

First raised: 2026-05-07
Last update: 2026-05-14

Review concern: unit-tests intermittently fail around timestamp-sensitive release markers

## Change

Documents a quarantine path for the release marker test without proving the root cause.

## Recommended next step

Freeze the clock in tests instead of quarantining the assertion permanently.
