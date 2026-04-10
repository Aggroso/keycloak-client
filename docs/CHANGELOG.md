# Changelog

## Unreleased

### Added (consumer-facing)

- **`KeycloakClient(access_token_provider=...)`** — pluggable async Bearer for Admin API calls while OIDC routes that use `auth_required=False` stay unchanged.
- **`KeycloakClientConfig.public_base_url`** — browser-facing Keycloak base for `services.bff.build_login_url`; Admin/token traffic still uses `base_url`.
- **`token_endpoint_grant` / `resource_owner_username` / `resource_owner_password`** — optional resource-owner-password (ROPC) path on `AuthProvider`, with **`fetch_resource_owner_password_token`** for one-shot token exchange (documented security caveats).
- **Idempotent provisioning** — `ensure_realm`, `ensure_client_by_client_id`, `ensure_realm_role`, `ensure_user_by_username`, `ensure_protocol_mapper` (package exports).
- **`sync_support.run_async`** — run a single coroutine from sync scripts.
- **`docs/SESSION_INHERITANCE.md`** — threat model and minimal parent→child trust-handoff notes for `InheritanceService`.

### Documentation

- Expanded **`docs/CONSUMER_INTEGRATION_REQUIREMENTS.md`** (library vs app-owned table, happy path, dual URL, tag-aligned install `v0.1.2`).
- README “does not do” clarifies redirect URI policy and post-logout app cleanup.
- **`docs/SERVICE_USAGE.md`**: optional config (`public_base_url`, injected Bearer, ROPC), provisioning helpers, `run_async`, links to consumer + session inheritance docs.

### Earlier

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
