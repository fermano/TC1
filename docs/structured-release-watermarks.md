# Structured release watermarks

Current exporters publish release watermark state under
`watermarks.release`, with an opaque `id` and a lifecycle `phase`. The
structured reader is intentionally a parsing boundary: consumers decide which
phases are meaningful for their own release contract.

The next package line uses this representation directly. Compatibility behavior
for older release branches is owned by their release adapters.
