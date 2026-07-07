# Release region selection

Legacy release callers pass a requested region, an allowlist, and a default.
Aliases are normalized before comparison. Blank or unsupported requests use the
configured default, which must itself appear in the normalized allowlist.

Selection returns the canonical region string used by existing deployment
scripts.
