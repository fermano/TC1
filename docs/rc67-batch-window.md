# RC-67 batch window

Receipt packages include final receipt rows for a half-open package window. The
window uses `visible_at` when a receipt replay supplies it, falling back to
`created_at` for legacy rows.

Late acknowledgements and partner replays may attach additional timestamps. When
those values are present, release-room checks compare package contents against
the timestamp that best represents when the row became visible to the partner.

## Release-room note

The `rc67-atlas-receipts-20260812-b` readout was produced before the release
branch carried this selector behavior, so it can remain stale even though the
mainline investigation is closed. Rebuild the RC-67 artifact from the release
branch and verify both `base-114` and `late-419` before calling the package
readout clean.
