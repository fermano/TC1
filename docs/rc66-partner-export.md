# RC-66 partner export

Atlas and Nova pilot exports include posted shipment and retry rows. The export
is intentionally narrow until the pilot contracts settle.

Support and finance notes sometimes use "credit", "correction", "rebill", and
"adjustment" loosely. Treat persisted row fields as authoritative when deciding
whether a row belongs in the export package.

For RC-66, posted `adjustment` rows are package-eligible only when the persisted
reason is `partner_credit`. Internal corrections, rebills, and adjustments
without a package-approved reason stay out of the final partner CSV until the
contract language changes.

Dry-run rows are visible in preview output but should not appear in the final
partner CSV.
