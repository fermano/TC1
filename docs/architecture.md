# TC1 architecture notes

TC1 models a small operations surface:

- service helpers expose owner normalization and severity ranking
- config captures release and review policy defaults
- docs provide runbook and release review context
- tests keep baseline behavior anchored for synthetic PRs

Most future changes in this repository are intentionally lightweight so the pull-request
workflow state is more important than the implementation itself.
