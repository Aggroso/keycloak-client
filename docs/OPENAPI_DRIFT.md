# OpenAPI drift checks

The script `scripts/check_keycloak_openapi_drift.py` verifies that **admin REST** operations referenced by the SDK’s v1 `ROUTE_SPECS` still exist in Keycloak’s published Admin OpenAPI document.

## What is checked

- **Source of truth:** `ROUTE_SPECS` in `python/src/keycloak_client/raw/*.py` (same set CI uses).
- **Compared against:** JSON OpenAPI from Keycloak docs (HTTP GET).
- **Scope:** Paths under `/admin/...` only. OIDC runtime paths (`/realms/{realm}/protocol/openid-connect/...`) are listed in raw modules for visibility but are **not** in the Admin OpenAPI spec and are **skipped** by the checker.

## Running locally

From the repository root (with the package importable):

```bash
cd /path/to/keycloak-client
python -m pip install -e "./python[dev]"
python scripts/check_keycloak_openapi_drift.py
```

Optional: point at a specific OpenAPI JSON URL:

```bash
export KEYCLOAK_OPENAPI_URL="https://www.keycloak.org/docs-api/latest/rest-api/openapi.json"
python scripts/check_keycloak_openapi_drift.py
```

## Default URL

- **Default:** `https://www.keycloak.org/docs-api/latest/rest-api/openapi.json` (defined in the script).
- Versioned URLs under `docs-api/<version>/rest-api/openapi.json` may be missing for some releases; when a stable URL exists for your target Keycloak version, set `KEYCLOAK_OPENAPI_URL` in CI or locally to pin the check.

## CI

Workflow: `.github/workflows/python-ci-release.yml`, job **`openapi-drift`**. It installs the Python package in editable mode and runs the script (network fetch to Keycloak docs).

## When Keycloak upgrades

Follow [`KEYCLOAK_UPGRADE_WORKFLOW.md`](./KEYCLOAK_UPGRADE_WORKFLOW.md): bump the Keycloak image in CI and local compose, run drift + unit + integration tests, then document any API or SDK adjustments.
