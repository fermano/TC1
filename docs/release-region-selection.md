# Release region selection

TC1 records release selection as an immutable `RegionDecision` produced from a
`RegionPolicy`. Aliases are canonicalized for requested, allowed, and default
regions.

A missing or blank request uses the policy default. An explicit region outside
the allowlist is rejected rather than silently changing deployment geography.
The default must itself belong to the normalized allowlist.

The policy form `resolve_release_region(policy, value) -> RegionDecision` is
the only supported public interface.


## Transition payloads

The current release payload may contain region and a compatibility region_hint.
A nonblank region remains authoritative. When that field is blank or omitted
during the transition, a nonblank region_hint is resolved under the same policy.
If neither has a value, the policy default is used. Explicit disallowed values
remain errors; a compatibility field does not silently change an explicit
current selection.
