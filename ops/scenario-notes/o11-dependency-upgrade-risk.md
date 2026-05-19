# Dependency upgrade risk

Scenario type: dependency upgrade risk
Simulated opened: 2026-05-06
Simulated last activity: 2026-05-13
Expected blocker: pytest upgrade changes collection behavior and could hide fixture failures
Risk level: high
Linear tracking: yes

## Change

Proposes bumping the test runner without documenting the compatibility check.

## Recommended next step

Run the full fixture validation matrix and pin a rollback version before approval.
