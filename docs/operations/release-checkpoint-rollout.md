# Release checkpoint rollout

Changes to checkpoint persistence require focused store/model tests, the full
repository suite, repository baseline verification, diff checks, and required
GitHub CI on the proposed head.

Migration and mixed-version fixtures in the repository define the supported
storage boundary. When those fixtures and required checks pass, this TC1 path
does not require a separate production soak or approving review before merge.
