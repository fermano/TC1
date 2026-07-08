# Artifact selection cache

Selected artifacts are cached during a worker process by release ID and
normalized target platform. Repeated deployment steps for the same release and
platform reuse the same candidate object, while different platforms are selected
independently. Legacy release-only cache entries are ignored after upgrading to
the platform-scoped selector.

Release coordination owns clearing the cache between release runs. The rc-42
repository recovery is owned by Fernando Mano in EXP-42.

If a rebuilt manifest does not contain the expected distinct target digests,
keep promotion held and rc-41 active. Clear the worker cache or use a fresh
worker before retrying. Do not roll back only the platform-scoped cache key and
retry rc-42, because the release-only key can reuse one target's artifact for a
different target.
