# RC-57 checkpoint envelopes

Release promotion workers persist checkpoint envelopes and may resume them after
a process replacement. The rollback worker remains part of the supported
release path.

Format changes are evaluated against persisted rows, promotion behavior, and
the rollback reader. The repository tests are the source of executable
compatibility behavior.
