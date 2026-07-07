# Intake service

The intake helpers keep support handoff parsing separate from release coordination code.

- Queue retry settings may be inherited from workspace configuration.
- Handoff records remain in the order copied from support notes.
- Release markers are normalized before they are included in status updates.

Intake now emits immutable `HandoffRecord` values with a canonical `signal_id`.
Filtering normalizes severity, owner, identifier, and summary values and returns
records rather than exposing caller-owned dictionaries to downstream release
coordination code.

During the Support cutover, intake also accepts legacy dictionaries that use
`event_id` or `signal_id`. When both are present, their non-blank trimmed values
must match. Every accepted input still produces an immutable `HandoffRecord`.

Callers may opt into replay reconciliation with
`filter_handoff_rows(..., collapse_retries=True)`. Repeated non-blank identifiers
keep their first list position while later copies contribute the highest known
severity and the latest non-blank owner and summary. Missing or blank identifiers
remain separate because TC1 cannot establish their identity. Severity filtering
runs after replay reconciliation so a corrected escalation is not hidden.

Changes to these helpers should stay focused and include regression coverage for edge cases.
