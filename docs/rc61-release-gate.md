# RC-61 release gate

The RC-61 release gate summarizes required check rows before promotion.

Required checks in failed, blocked, or manual-hold states must hold the release.
Optional checks remain advisory.

During client rollout, operators may see slightly different spellings from the
release room and worker replay clients. Code behavior, not runbook spelling,
defines whether a required row holds the release.
