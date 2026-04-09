# Release Process

## Versioning
- Use semantic versioning.
- Tag releases as `vX.Y.Z`.

## Steps
1. Run local pre-release validation:
   - `scripts/pre_release_validation.sh`
2. For real-environment integration validation, export and run:
   - `KEYCLOAK_INTEGRATION=1`
   - `KEYCLOAK_BASE_URL=<staging-keycloak-url>`
   - `KEYCLOAK_CLIENT_ID=<client-id>`
   - `KEYCLOAK_CLIENT_SECRET=<secret-or-empty>`
   - `scripts/pre_release_validation.sh`
3. Ensure CI is green for quality, integration, OpenAPI drift, and security checks.
4. Update changelog and compatibility notes.
5. Create release tag.
6. CI publishes package to private Python registry.

See also:

- `docs/RELEASE_PIPELINES.md`
- `docs/PRIVATE_REGISTRY_CONSUMER_SETUP.md`

## Rollback
- If publish is bad, deprecate compromised version and release patched version.
