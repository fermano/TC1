# RC-71 route invoice manifest

RC-71 route invoice packaging emits invoice rows for partner routes from the release branch artifact.

Current field names expected from the release artifact:

- `tenant_id`
- `invoice_id`
- `route_id` for the current adapter
- `partner_id` for older replay rows
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
- Retraction-like states should be interpreted by event order for the same route and invoice, not globally across all routes. A void on `route_id=card` must not suppress a posted `route_id=bank` row for the same invoice.
- Release order should remain stable enough for downstream diff/readout tooling; avoid reshuffling rows solely to make implementation easier.

A QA export sometimes called the route field `partner_route`, but the release adapter currently emits `route_id` and legacy replay emits `partner_id`.
