# Release Pipelines

This document tracks release pipeline readiness by language package.

## Python package pipeline (implemented, Option B: Git tag distribution)

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
- `release-artifacts` job (tag-gated)
  - Build package
  - Upload `dist/*` artifacts to GitHub Actions run artifacts

Required secrets:

- None for package publishing (artifact upload only)

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



## Consumer install (Git tag)

Use tagged versions directly from GitHub:

```bash
pip install "git+https://github.com/Aggroso/keycloak-client.git@v0.1.2#subdirectory=python"
```
