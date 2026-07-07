# Release checkpoint persistence

During a rolling deployment, TC1 keeps the legacy `checkpoints` table and the
current `checkpoint_state` table. New writes are copied to both tables so
workers on the older package can resume from the latest generation and offset.

Current readers prefer the new table and fall back to legacy state when migration
has not populated it yet.
