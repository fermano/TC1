# TC1 architecture notes

TC1 models a small operations surface:

- service helpers expose owner normalization and severity ranking
- config captures release and review policy defaults
- docs provide runbook and release review context
- tests keep baseline behavior anchored around core service helpers

Most future changes in this repository are intentionally lightweight so pull-request
state, review notes, and release context remain easy to inspect.
