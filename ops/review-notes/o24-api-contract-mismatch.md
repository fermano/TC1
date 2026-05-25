# API contract mismatch

First raised: 2026-05-12
Last update: 2026-05-17

Review concern: downstream workflow expects `severity`, but note proposes `risk_level`

## Change

Captures a naming mismatch that can break workflow parsers consuming PR metadata.

## Recommended next step

Align on the field name and add compatibility notes before merge.
