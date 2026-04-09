# Release Pipelines

This document tracks release pipeline readiness by language package.

## Python package pipeline (implemented)

Workflow: `.github/workflows/python-ci-release.yml`

- `quality` job
  - Ruff
  - Mypy
  - Unit tests
  - Wheel/sdist build
- `openapi-drift` job
  - `scripts/check_keycloak_openapi_drift.py`
- `integration-keycloak` job
  - Keycloak container startup + health wait
  - Integration tests with `KEYCLOAK_INTEGRATION=1`
- `publish-private` job (tag-gated)
  - Build package
  - Upload via `twine` to private registry

Required secrets:

- `PRIVATE_PYPI_USERNAME`
- `PRIVATE_PYPI_PASSWORD`
- `PRIVATE_PYPI_REPOSITORY_URL`

## TypeScript package pipeline (deferred)

Current status: deferred until a real `typescript/` package lands in this repository.

Planned pipeline once package exists:

- install + lockfile verification
- lint
- typecheck
- unit tests
- integration tests (where applicable)
- tag-gated private npm publish

Required future secrets (example):

- `NPM_TOKEN` (or registry-specific token secret)

## Release validation before tagging

Run from repo root:

```bash
scripts/pre_release_validation.sh
```

For real environment integration:

```bash
KEYCLOAK_INTEGRATION=1 \
KEYCLOAK_BASE_URL=https://<keycloak-host> \
KEYCLOAK_CLIENT_ID=<bootstrap-client-id> \
KEYCLOAK_CLIENT_SECRET=<bootstrap-client-secret> \
scripts/pre_release_validation.sh
```

