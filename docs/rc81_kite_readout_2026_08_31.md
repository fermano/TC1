# KiteBank RC81 readout note

The 18:20 BRT dashboard smoke shows the transfer-row count matching yesterday's candidate. That check does not inspect `holdSeconds` on the partner artifact row.

Ambiguous status: support marked the card green because the total row count recovered, while release notes still say the `kitebank/ach/tr-884` action should not be considered verified until the artifact row is inspected.
