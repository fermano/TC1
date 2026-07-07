# Intake service

The intake helpers keep support handoff parsing separate from release coordination code.

- Queue retry settings may be inherited from workspace configuration.
- Handoff records remain in the order copied from support notes.
- Release markers are normalized before they are included in status updates.

Intake now emits immutable `HandoffRecord` values with a canonical `signal_id`.
Filtering normalizes severity, owner, identifier, and summary values and returns
records rather than exposing caller-owned dictionaries to downstream release
coordination code.

Changes to these helpers should stay focused and include regression coverage for edge cases.
