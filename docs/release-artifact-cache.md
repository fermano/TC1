# Artifact selection cache

Selected artifacts are cached during a worker process so repeated deployment
steps for a release reuse the same candidate object. Release coordination clears
the cache between release runs.
