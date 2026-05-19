# API contract mismatch

Scenario type: API contract mismatch
Simulated opened: 2026-05-12
Simulated last activity: 2026-05-17
Expected blocker: downstream workflow expects `severity`, but note proposes `risk_level`
Risk level: high
Linear tracking: yes

## Change

Captures a naming mismatch that can break workflow parsers consuming PR metadata.

## Recommended next step

Align on the field name and add compatibility notes before merge.
