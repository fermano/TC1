# TC1 operations runbook

## PR triage

1. Check the scenario metadata block in the PR body.
2. Verify whether Linear tracking exists.
3. Prioritize critical and high-risk release, security, and migration changes.
4. Add an owner comment when the next action is unclear.

## Release validation

Before marking a release-facing PR as ready, confirm:

- CI status is green or the failing check is documented as flaky.
- Test coverage exists for changed behavior.
- Operational runbooks match the implementation.
- Rollback and owner information are present.

## Linear hygiene

Every merged PR should have a completed Linear issue. Open PRs may intentionally omit
Linear tracking so workflow agents can detect missing work items.
