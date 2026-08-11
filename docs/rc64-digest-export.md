# RC-64 digest export

The RC-64 digest export candidate check is used by the release-room replay
before a digest package is promoted. The check should include active email and
SMS contacts once per tenant/contact/channel pair.

Rows in terminal or suppressed states are not exported. Operator notes may use
"retired", "retired contact", or "archive replay" when describing contacts that
should no longer receive digest messages; the code path should stay focused on
candidate eligibility rather than broad contact lifecycle cleanup.
