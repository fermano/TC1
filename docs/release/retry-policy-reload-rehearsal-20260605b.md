# Retry Policy Reload Rehearsal

Repository: TC1
Date: 2026-06-05

Release rehearsal cases:

- A missing retry override inherits the workspace default.
- An explicit retry override of 0 means retries are disabled for the handoff.
- Positive overrides should survive policy reload unchanged.

The checklist owner should confirm these examples against the loader path before release notes cite them as verified.
