# Changelog

## Unreleased
- Release/distribution strategy switched to Option B (Git tag install):
  - tag workflow builds and uploads release artifacts (`release-artifacts` job)
  - consumer install via `pip install "git+https://...@vX.Y.Z#subdirectory=python"`
- Phase 8 documentation and release-readiness:
  - Expanded root and Python package READMEs (`README.md`, `python/README.md`)
  - Added route-method permission map (`docs/ROUTE_METHOD_PERMISSION_MAP.md`)
  - Added release/consumer docs (`docs/RELEASE_PIPELINES.md`, `docs/PRIVATE_REGISTRY_CONSUMER_SETUP.md`)
  - Added Phase 8 completion record in `docs/IMPLEMENTATION_PLAN.md`
  - TypeScript package/pipeline docs explicitly deferred until `typescript/` package exists
- Phase 7 integration, compatibility, and CI:
  - GitHub Actions: quality (Ruff, Mypy, unit tests, wheel), OpenAPI drift job, Keycloak integration job
  - `scripts/check_keycloak_openapi_drift.py` and docs: `OPENAPI_DRIFT.md`, `KEYCLOAK_UPGRADE_WORKFLOW.md`
  - Integration testing / compatibility docs updated; `docker-compose.keycloak.yml` aligned with CI image tag
  - TypeScript lint/CI matrix deferred until `typescript/` package exists (recorded in `IMPLEMENTATION_PLAN.md`)
- Phase 6 security hardening:
  - Expanded redaction and BFF event safety tests; transport retry and 403 coverage
  - `allow_dangerous_operations` config, `dangerous_realm_logout_all`, realm rollback gate
  - `docs/KEYCLOAK_LEAST_PRIVILEGE.md` and `docs/SECURITY_MODEL.md` updates (inheritance controls)
- Phase 5 production-readiness scaffolding added:
  - Integration harness and tests
  - Security/fail-closed regression checks
  - Compatibility policy and docs
  - CI build/publish workflow for private registry
