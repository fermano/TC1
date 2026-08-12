# RC-70 invoice readout

The invoice candidate is considered promotable only when the readout artifact points at the final release branch.

Required readout fields:

- `artifact_id`
- `source_ref=release/rc-70`
- `source_sha`
- `package_kind=invoice`
- matching `row_count` and `expected_row_count`
- matching checksum when an expected checksum is present

A shadow, preview, or dry-run ref can be useful for comparison, but it is not release evidence by itself. If a later readout from `release/rc-70` matches the row count and checksum, older shadow-source records should be treated as stale unless a newer mismatch appears.

Current known-good sample for final readout checks:

```text
artifact_id=rc70-invoice-east-20260812-g
source_ref=release/rc-70
package_kind=invoice
row_count=260
expected_row_count=260
checksum=8c41e7b
expected_checksum=8c41e7b
smoke=passed
```
