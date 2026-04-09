# Keycloak upgrade workflow

Use this when moving the SDK’s validated Keycloak target (CI image, local integration harness, or documented compatibility).

## 1. Decide the new target version

- Prefer a **specific image tag** (for example `quay.io/keycloak/keycloak:26.0.7`) in GitHub Actions and `python/tests/integration/docker-compose.keycloak.yml` so CI and local runs stay aligned.
- Record the change in release notes or the changelog when it affects consumers.

## 2. Pin OpenAPI drift (optional but recommended)

- If Keycloak publishes `openapi.json` for that version under `https://www.keycloak.org/docs-api/<version>/rest-api/openapi.json`, set `KEYCLOAK_OPENAPI_URL` for the **`openapi-drift`** CI job to that URL.
- If the versioned URL is unavailable, keep the default **latest** OpenAPI URL and treat drift as “tracks current docs”; still run integration tests against the pinned container image.

## 3. Run checks in order

1. **OpenAPI drift:** `python scripts/check_keycloak_openapi_drift.py` (or rely on CI job `openapi-drift`).
2. **Lint and types:** `cd python && ruff check src/keycloak_client && mypy src/keycloak_client`.
3. **Unit tests:** `cd python && pytest -q tests --ignore=tests/integration`.
4. **Integration tests:** start Keycloak (see [`INTEGRATION_TESTING.md`](./INTEGRATION_TESTING.md)), set `KEYCLOAK_INTEGRATION=1`, then `cd python && pytest -q tests/integration`.

## 4. Breaking Admin API changes

- **SDK contract changes** (removed or renamed operations, incompatible paths): require a **minor or major** semver bump per language package, migration notes, and an explicit compatibility note in release documentation.
- **Approval:** breaking changes to the public Python API should be reviewed by maintainers responsible for the client libraries and security posture (`docs/SECURITY_MODEL.md`, `docs/KEYCLOAK_COMPATIBILITY_POLICY.md`).

## 5. Documentation

- Update [`KEYCLOAK_COMPATIBILITY_POLICY.md`](./KEYCLOAK_COMPATIBILITY_POLICY.md) if support or retest policy changes.
- Update [`INTEGRATION_TESTING.md`](./INTEGRATION_TESTING.md) if CI job names, env vars, or image tags change.

See also: [`OPENAPI_DRIFT.md`](./OPENAPI_DRIFT.md).
