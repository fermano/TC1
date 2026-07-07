# Promotion lease fencing

Promotion workers acquire a lease containing a monotonically increasing fence.
Before publishing, a worker checks that its owner and fence still match the
current row and that the lease has not expired. Takeover and renewal advance the
fence under an immediate SQLite transaction.
