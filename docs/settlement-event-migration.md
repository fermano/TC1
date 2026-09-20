# Structured settlement events

Current exporters consume `settlement.token`, `settlement.state`, and
`settlement.replaces`. A committed structured event supplies the current
reference. A retracted event is not emitted by current exporters.

Release branches may have older consumers and transitional data. This document
does not define their compatibility policy; release adapters must retain or
replace supported behavior deliberately.
