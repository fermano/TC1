# RC-62 customer pause gate

The RC-62 sender filters paused customer deliveries before dispatch.

Paused rows may arrive from several clients during rollout. Older scheduler rows
may omit state and are treated as active for compatibility. Current behavior is
owned by the repository tests.
