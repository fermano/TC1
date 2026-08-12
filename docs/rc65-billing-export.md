# RC-65 billing export

The RC-65 billing export includes billable delivery and retry events once per
`tenant_id` / `event_id` / `event_type` tuple.

Preview, sandbox, and test-mode activity should not be billed. Older producer
rows may omit environment metadata; those rows remain eligible unless another
explicit non-billable signal is present.

Support notes may use "sandbox", "test mode", or "preview-run" loosely. Runtime
selection should follow persisted fields rather than broad wording cleanup.
