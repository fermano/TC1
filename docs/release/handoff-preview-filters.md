# Handoff Preview Filters

A one-off preview can suppress lower-severity rows without changing workspace defaults.

Example:

```text
handoff preview --minimum-severity high
```

Supported values are `low`, `medium`, `high`, and `critical`. The option affects only the current preview and preserves the original row order.
