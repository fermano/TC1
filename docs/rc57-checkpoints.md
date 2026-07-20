# RC-57 checkpoint envelopes

Release promotion workers persist checkpoint envelopes and may resume them after
a process replacement. The rollback worker remains part of the supported
release path.

Format changes are evaluated against persisted rows, promotion behavior, and
the rollback reader. The repository tests are the source of executable
compatibility behavior.

During the RC-57 rolling window, writers keep the schema-one envelope so the
rollback worker can read newly persisted checkpoints. Generation and checksum
fields are additive: a pre-generation schema-one row resumes at generation
zero, while a newly written row binds the cursor, generation, and optional
rollback tag in its checksum.

The current worker also accepts the transitional schema-two envelope emitted
by the earlier generation backport. Its next successful resume rewrites that
checkpoint as schema one. Store initialization adds the missing generation
column in place so existing release rows and routing data remain available.
