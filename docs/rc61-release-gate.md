# RC-61 release gate

The RC-61 release gate summarizes required check rows before promotion.

Required checks in failed, blocked, or manual-hold states must hold the release.
Optional checks remain advisory.

The canonical persisted state name is `manual_hold`. During client rollout,
operators may also see human-readable labels from release-room tools. Code
behavior, not runbook spelling, defines whether a required row holds the release.
