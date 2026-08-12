# TC1 delivery pause windows

Delivery pause windows are small records shared by retry workers, manual drain jobs, and admin pause/resume controls.

Current fields:

- `tenant_id`: tenant owning the work item.
- `route_id`: preferred current route identifier.
- `destination_id`: older route identifier accepted as fallback.
- `hold_seconds`: explicit pause duration. Missing or blank values inherit the workspace default.

The normalized window is intentionally compact because it is copied into retry/drain logs and Linear incident notes.
