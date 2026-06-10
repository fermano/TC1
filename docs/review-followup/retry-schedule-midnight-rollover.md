# Retry Schedule Midnight Rollover

Release rehearsal examples:

- A retry scheduled at 23:59:30 UTC with a 45-second delay runs at 00:00:15 UTC on the next date.
- An explicit retry budget of 0 still means no retry is scheduled.
- An omitted retry override continues to inherit the workspace default.

The release checklist should cite these examples only after the loader and scheduler boundary is covered directly.
