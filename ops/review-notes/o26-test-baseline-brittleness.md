# Test baseline brittleness

First raised: 2026-05-13
Last update: 2026-05-18

Review concern: tests depend on exact wall-clock output

## Change

Adds validation guidance that may become flaky when run near minute boundaries.

## Recommended next step

Inject a deterministic clock in tests and avoid asserting raw timestamps.
