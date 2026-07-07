# Intake service

The intake helpers keep support handoff parsing separate from release coordination code.

- Queue retry settings may be inherited from workspace configuration.
- Handoff rows remain in the order copied from support notes.
- Release markers are normalized before they are included in status updates.

When support delivery retries repeat a non-blank `event_id`, callers may use
`filter_handoff_rows(..., collapse_retries=True)` to keep the first copied row
for that identifier. Rows without identifiers stay separate because TC1 cannot
establish identity for them.

Changes to these helpers should stay focused and include regression coverage for edge cases.
