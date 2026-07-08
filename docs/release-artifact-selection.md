# Release artifact selection

Release candidates may publish platform-specific and universal artifacts. The
selector normalizes runner aliases before preferring an exact platform entry and
otherwise using a universal entry.

The Linux runner aliases used by rc-42 map as follows:

- `linux/x86_64` maps to `linux-amd64`;
- `linux/aarch64` maps to `linux-arm64`.

Candidate platform values are normalized by the same rules. Selection caching
is scoped to the release ID plus the normalized platform so a multi-platform
release cannot reuse an amd64 selection for arm64, or the reverse.
