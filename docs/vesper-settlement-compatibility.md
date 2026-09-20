# Vesper RC1 settlement compatibility

Vesper RC1 preview and reconciliation exports share the release adapter in
`vesper_settlement_export`. The RC1 package still receives a top-level
`settlement_token` with `settlement_phase: committed`.

A structured settlement event is being introduced on mainline. Its parser may
be useful to an RC1 recovery, but replacing the RC1 package interface or
changing both consumers independently requires a release-specific decision.
