# RC-71 route invoice manifest

RC-71 route invoice packaging emits invoice rows for partner routes from the release branch artifact.

Current field names seen during the release-room window:

- `tenant_id`
- `invoice_id`
- `route_id` for the current adapter
- `partner_id` for older replay rows
- `partner_route` in one QA export screenshot
- `sequence` or `event_sequence`
- `state`
- `amount_cents`

The manifest identity gate expects:

```text
source_ref=release/rc-71
package_kind=route_invoice
row_count == expected_row_count
checksum == expected_checksum when present
```

Operational notes:

- Route identity should be preserved; the same `invoice_id` can be valid on two partner routes.
- Retraction-like states should be interpreted by event order for the same route and invoice, not globally across all routes.
- Release order should remain stable enough for downstream diff/readout tooling; avoid reshuffling rows solely to make implementation easier.

Open question: `partner_route` appeared in QA but has not been confirmed in the final release artifact.
