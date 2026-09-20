# Helios RC4 invoice export

Helios RC4 reads the release watermark through its release adapter. The current
package line continues to emit the legacy top-level representation to downstream
invoice consumers. Structured watermark work is being introduced on mainline
separately from this release branch.

For the transition metadata shape, the adapter preserves any nonblank top-level
`release_watermark`. When that legacy field is blank or absent, it may use
`watermarks.release.id` only when `watermarks.release.phase` is `final`.
Prepared structured watermarks do not override an existing release reference.
