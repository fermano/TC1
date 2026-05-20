# TC1 operations runbook

## PR triage

1. Review the current diff, check status, labels, and latest discussion.
2. Verify whether any linked work item reflects the same blocker and next owner.
3. Prioritize critical release, security, migration, and customer-impact changes.
4. Add an owner comment when the next action is unclear.

## Release validation

Before marking a release-facing PR as ready, confirm:

- CI status is green or the failing check has an accepted owner decision.
- Test coverage exists for changed behavior.
- Operational runbooks match the implementation.
- Rollback and owner information are present.

## Tracking hygiene

Merged PRs should have a completed work item. Open PRs should either link to active tracking or make the missing owner explicit in the PR discussion.
