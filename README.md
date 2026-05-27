# TC1

TC1 is a small operations-service repository used for release, incident, and review process exercises. The code is intentionally compact so changes are easy to inspect, while the surrounding docs and configuration model common engineering operations work.

## Local checks

```bash
python -m pytest
```

## Repository layout

- `src/tc1_service.py` contains service primitives used by tests and examples.
- `tests/` contains regression coverage for service behavior.
- `config/operations.yml` stores reviewer, release, and incident-routing defaults.
- `docs/` stores runbooks, release notes, and operating guidance.

## Weekly digest settings

Muted projects stay out of weekly digest email summaries. Muting a project does
not change regular in-app notification delivery, so teams can quiet the digest
without hiding active workspace activity.

## Triage notes

Evaluate PRs from the current diff, check status, review discussion, linked work items, and release context. When a change is blocked, leave the blocker in the PR thread and keep any external tracker aligned with the current owner and next action.
