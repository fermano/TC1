# Release checklist

- Confirm release marker generation before cutoff.
- When a channel is copied from support notes, verify the generated marker keeps the normalized slug.
- Confirm the default `internal` marker still holds when no channel is supplied.
- Check incident-routing configuration.
- During cutover handoff, keep release-note owners and review-queue wording aligned before cutoff.
- Verify migration confidence and rollback notes.
- Confirm documentation links in PRs and Linear issues.
- Require the retention-delete policy gate to pass on protected rows before cleanup merges.
- Tag unresolved risks before release cutoff.
