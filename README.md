# TC1 synthetic SWE operations fixture

TC1 is a deliberately small repository used to test agentic software-engineering workflows.
The code is intentionally simple; the interesting surface is the operational metadata around
pull requests, Linear tracking, stale reviews, blocker comments, and release triage.

## Local checks

```bash
python -m pytest
python scripts/verify_fixture.py
```

## Repository layout

- `src/tc1_service.py` contains the tiny service primitives used by test changes.
- `tests/` contains regression tests for the service behavior.
- `config/operations.yml` stores reviewer, release, and incident-routing defaults.
- `docs/` stores runbooks, release notes, and fixture operating guidance.

## Fixture conventions

Synthetic pull requests include scenario metadata in the PR body:

- Scenario type
- Simulated opened date
- Simulated last activity date
- Expected blocker
- Risk level
- Linear tracking status

The metadata is intentionally redundant so future workflow tests can sort and reason over
GitHub state, commit dates, PR bodies, labels, and Linear issue links.
