# Intake service

The intake helpers keep support handoff parsing separate from release coordination code.

- Queue retry settings may be inherited from workspace configuration.
- An explicit retry budget of `0` disables retries and must not be treated as inheritance.
- Handoff rows remain in the order copied from support notes.
- Release markers are normalized before they are included in status updates.

Changes to these helpers should stay focused and include regression coverage for edge cases.
