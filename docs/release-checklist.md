# Release checklist

- Confirm release marker generation before cutoff.
- When a channel is copied from support notes, verify the generated marker keeps the normalized slug.
- Confirm the default `internal` marker still holds when no channel is supplied.
- Check incident-routing configuration.
- During cutover handoff, keep release-note owners and review-queue wording aligned before cutoff.
- For empty release-note handoffs, confirm the fallback owner still appears in the summary.
- Verify migration confidence and rollback notes.
- Confirm documentation links in PRs and Linear issues.
- Tag unresolved risks before release cutoff.
