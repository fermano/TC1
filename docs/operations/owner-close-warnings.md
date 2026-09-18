# Owner close warnings

A warning is scheduled from the configured close timestamp. A manual close or reopen
recorded at or before the scheduled warning time suppresses the warning. The close
timestamp itself is never moved by this decision.

Lifecycle event timestamps are compared as UTC instants. Support screenshots and
workstation timestamps are diagnostic context only; they are not a substitute for
the recorded event timestamp.

A close or reopen may arrive with a different wall-clock zone than the support case display; compare the normalized recorded instant rather than the display footer.
