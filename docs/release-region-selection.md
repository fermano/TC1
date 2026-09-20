# Release region selection

TC1 records release selection as an immutable `RegionDecision` produced from a
`RegionPolicy`. Aliases are canonicalized for requested, allowed, and default
regions.

A missing or blank request uses the policy default. An explicit region outside
the allowlist is rejected rather than silently changing deployment geography.
The default must itself belong to the normalized allowlist.

The legacy call form
`resolve_release_region(value, allowed_regions, default_region) -> str` remains
available for one release window. It is deprecated; callers should migrate to
`resolve_release_region(policy, value) -> RegionDecision`. The compatibility
form builds a policy and delegates to the same decision engine before returning
the selected canonical region string, so normalization and validation do not
diverge between the two paths.


## Solstice transition packets

Solstice RC2 packets can carry both the current `region` field and the
compatibility `region_hint` field. A nonblank current region remains
authoritative. When the current region is blank or omitted during the
transition, a nonblank compatibility hint is resolved through the same
allowlist and default policy. If neither field has a value, the policy default
is used.
