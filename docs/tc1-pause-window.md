# TC1 delivery pause windows

Delivery pause windows are small records shared by retry workers, manual drain jobs, and admin pause/resume controls.

Current fields:

- `tenant_id`: tenant owning the work item.
- `route_id`: preferred current route identifier.
- `legacy_route_id`: migration-era route identifier accepted before older destination data.
- `destination_id`: oldest route identifier accepted as fallback only.
- `hold_seconds`: explicit pause duration. Missing or blank values inherit the workspace default.
- `scope_key`: normalized `tenant_id:route_id` identity used by retry and drain logs.

Current route identity order is `route_id`, then `legacy_route_id`, then `destination_id`. Preserving that order matters because old drain exports may carry both legacy and destination values during replay.

The normalized window is intentionally compact because it is copied into retry/drain logs and Linear incident notes.
