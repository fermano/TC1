# Delivery queue names

Delivery submissions use the canonical queue names `priority`, `standard`, and `bulk`.

The legacy `general` value is not accepted by the current ingestion API. Older mobile adapters must migrate to `standard`; this document does not introduce a compatibility alias.
