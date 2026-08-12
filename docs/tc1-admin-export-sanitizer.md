# TC1 admin export sanitizer

Admin/support export bundles must hide secrets before the bundle is copied into diagnostics, email, Slack, or support tooling.

Known safe identity fields:

- `tenant_id`
- `workspace_id`
- `connector_count`
- contact metadata such as `owner_email` and `secretary_email`
- hints that are explicitly non-secret, such as `public_token_hint`

Known secret fields include:

- `api_key`
- `access_token`
- `refresh_token`
- `client_secret`
- `signing_secret`
- `password`
- `private_key`
- nested connector `auth` fields using the same names

Operational constraint: sanitizing a bundle must not mutate the original parsed payload. The admin preview and audit review can render from the same object in a single request.
