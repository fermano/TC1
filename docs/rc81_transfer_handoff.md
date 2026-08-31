# RC81 transfer handoff

RC81 emits route-scoped transfer rows with `artifact_schema=rc81.transfer.v2` and an `operator_key` derived from the selected route, transfer, and final action.

The hold window uses the first non-null, non-empty value from `hold_seconds`, then the partner replay alias `holdSeconds`, then the workspace default. Numeric and string zero both mean immediate release. Missing or blank windows inherit the default; route identity still prefers `route_id`, then `destination_id`, then `primary`.

Recovery PR [#596](https://github.com/fermano/TC1/pull/596) combines the release-shaped partial fix with the alias semantics from prototype [#597](https://github.com/fermano/TC1/pull/597), while preserving the schema/operator fields added in `d6ee355`. The prototype's destination-shaped output is superseded, not copied into the release.

The dashboard count smoke on 2026-08-31 only checked row totals. It did not prove the KiteBank replay in [#595](https://github.com/fermano/TC1/issues/595): `kitebank/ach/tr-884` with `holdSeconds: "0"` must emit `hold_seconds=0`, `action=release`, and `operator_key=ach:tr-884:release`. The regression tests assert this full row and preserve the blank/default wire-route control. Readout PR [#598](https://github.com/fermano/TC1/pull/598) is context only, not the artifact fix.
