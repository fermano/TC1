# Release region selection

TC1 records release selection as an immutable `RegionDecision` produced from a
`RegionPolicy`. Aliases are canonicalized for requested, allowed, and default
regions.

A missing or blank request uses the policy default. An explicit region outside
the allowlist is rejected rather than silently changing deployment geography.
The default must itself belong to the normalized allowlist.
