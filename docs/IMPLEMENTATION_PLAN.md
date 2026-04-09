# Implementation plan: full Keycloak client libraries

This plan implements the expanded scope confirmed by the team: map Keycloak capabilities to Python and TypeScript methods with consistent, centralized security controls across all route families.

Primary requirements source: [`KEYCLOAK_CLIENT_LIBRARY_REQUIREMENTS.md`](./KEYCLOAK_CLIENT_LIBRARY_REQUIREMENTS.md).

## Goals

- Build production-grade Python and TypeScript Keycloak clients.
- Cover broad Keycloak route families (phased), not only BFF auth helper routes.
- Maintain BFF compatibility for existing `login/callback/refresh/logout/userinfo` workflows.
- Support cross-realm session inheritance as trusted authentication handoff with per-realm local sessions.
- Enforce consistent security and transport policy across all modules.
- Keep API compatibility sustainable as Keycloak versions evolve.

## Principles

- **Coverage by inventory:** every supported endpoint is mapped in a route inventory.
- **Two-layer SDK design:** raw route parity + high-level service methods.
- **Centralized security:** one auth/token/transport/redaction pipeline for all routes.
- **Server-first admin model:** admin features are backend-only; no browser secrets.
- **Version-aware:** support explicitly declared Keycloak versions.

## Repository layout (target)

```text
keycloak-client/
  README.md
  LICENSE
  docs/
    KEYCLOAK_CLIENT_LIBRARY_REQUIREMENTS.md
    IMPLEMENTATION_PLAN.md
    ROUTE_INVENTORY.md               # generated/maintained mapping table
    SECURITY_MODEL.md                # redaction, auth, retry, permissions
    BFF_CONTRACT.md                  # optional extracted BFF contract
  python/
    pyproject.toml
    src/keycloak_client/
      __init__.py
      config.py
      transport.py
      auth_provider.py
      errors.py
      models/
      raw/
      services/
      bff/
    tests/
  typescript/
    package.json
    tsconfig.json
    src/
      index.ts
      config.ts
      transport.ts
      authProvider.ts
      errors.ts
      models/
      raw/
      services/
      bff/
    tests/
```

## Phase 0 - foundation and decisions

### Locked decisions

| Decision area | Final value |
|---|---|
| v1 scope | Selected core route set only (`docs/SELECTED_ROUTES_AND_USE_CASES.md`, 61 routes). |
| v2+ scope | Expand toward full Keycloak route coverage using `docs/ROUTE_INVENTORY.md`. |
| Realm creation | Included in v1 runtime methods (guarded as high-risk operation). |
| Error style | Support both typed exceptions and result wrappers; default behavior is typed exceptions. |
| Keycloak support policy | Latest stable Keycloak only (v1). |
| Python package | `keycloak_client` |
| npm package | `@yourorg/keycloak-client` |
| Minimum Python | 3.11 |
| Minimum Node | 20 LTS |
| Versioning strategy | Independent semver per language package with aligned release notes. |
| Distribution strategy (v1) | Private/internal package registries only (no public PyPI/npm release in v1). |
| Delivery strategy (v1) | Python-first implementation for all selected routes; TypeScript split into backend-admin mirror (later) and frontend-safe auth subset only. |

### Phase 0 outputs

1. SDK boundaries and module split locked in docs:
   - Raw route-parity modules
   - High-level service modules
   - BFF compatibility module
   - Shared auth/transport/error core
2. Runtime and package defaults locked for Python and TypeScript.
3. Security baseline locked in `docs/SECURITY_MODEL.md`.
4. Release policy and breaking-change rules locked.
5. Phase 0 exit gate and acceptance checklist defined.

### Release and breaking-change policy (locked)

- Python and TypeScript packages are versioned independently using semver.
- A release in one language does not require a forced version bump in the other unless behavior parity changed.
- Breaking changes require:
  - major version increment in affected package
  - migration notes in changelog
  - explicit API compatibility note in release documentation
- Keycloak version bump releases must include:
  - OpenAPI diff summary
  - impacted service/module list
  - test coverage confirmation for changed route families
- v1 package publishing channel:
  - Python: private PyPI-compatible registry (for example Artifactory/Nexus/CodeArtifact/GitHub Packages)
  - TypeScript: private npm-compatible registry
  - public package publication deferred to a later approval milestone

## Phase 1 - route inventory and mapping model

1. Pull Keycloak OpenAPI from the official Admin REST docs.
2. Build `docs/ROUTE_INVENTORY.md` with:
   - endpoint + method
   - route family
   - SDK module + method name
   - request/response model names
   - required permissions hints
3. Classify endpoints:
   - v1 required
   - v2 expansion
   - optional/advanced
4. Ensure both Python and TypeScript use the same logical naming and structure.

Deliverable: complete v1 route inventory with explicit mapping coverage.

### Phase 1 completion record

- Route inventory created: `docs/ROUTE_INVENTORY.md`.
- Canonical source used: Keycloak official latest Admin REST OpenAPI.
- Coverage validation result:
  - OpenAPI operations: `387`
  - Inventory mapped operations: `387`
  - Missing operations: `0`
  - Extra/non-canonical operations: `0`
  - Python per-family name collisions: `0`
  - TypeScript per-family name collisions: `0`
- Phase 1 exit criteria status: **completed**.
- Transition recommendation: proceed to Phase 2 shared auth/transport/error core implementation.

## Phase 2 - shared architecture and security pipeline (Python-first)

Implement shared architecture in Python first, then mirror selectively to TypeScript:

1. **Config layer**
   - base URL(s), realm defaults, timeout, retry policy, TLS expectations.
2. **Auth provider**
   - confidential client token acquisition
   - cache + skew-aware refresh
   - concurrency-safe refresh lock
3. **Transport layer**
   - request execution
   - normalized headers
   - timeout/retry enforcement
   - centralized redaction in logs/errors
4. **Error layer**
   - one SDK error model per language
   - parse Keycloak errors and classify retryability

Deliverable: reusable Python platform components with unit tests for auth/transport/error behavior.

### Phase 2 route scope lock

Phase 2 implementation targets only the scoped core routes defined in:

- `docs/SELECTED_ROUTES_AND_USE_CASES.md`

Locked scope size:

- **61 routes total**

Implementation order inside Phase 2:

1. Authentication/token routes
2. User CRUD and lifecycle routes
3. Role and group routes
4. Client routes
5. Identity provider routes
6. Realm configuration routes

Out-of-scope for Phase 2:

- Any Admin API route not listed in `docs/SELECTED_ROUTES_AND_USE_CASES.md`
- Full 387-route coverage from `docs/ROUTE_INVENTORY.md`
- TypeScript full admin-route parity in this phase

### TypeScript safety split (locked)

TypeScript usage is split by runtime:

- **Frontend TypeScript (browser):**
  - Only frontend-safe auth subset:
    - `GET /realms/{realm}/protocol/openid-connect/auth`
    - `POST /realms/{realm}/protocol/openid-connect/token` (public-client/PKCE usage only)
    - `POST /realms/{realm}/protocol/openid-connect/logout`
    - `GET /realms/{realm}/protocol/openid-connect/userinfo`
    - `GET /realms/{realm}/protocol/openid-connect/certs`
    - `GET /realms/{realm}/.well-known/openid-configuration`
- **Backend TypeScript (Node):**
  - Eligible for admin-route mirror later (post Python stabilization).
- **Never allowed in browser:**
  - all `/admin/*` endpoints
  - `POST /realms/master/protocol/openid-connect/token`

### Phase 2 completion record

- Python package scaffold created under `python/` with:
  - `pyproject.toml`
  - core modules: `config.py`, `errors.py`, `redaction.py`, `auth_provider.py`, `transport.py`, `client.py`
  - raw family stubs in `python/src/keycloak_client/raw/`
- Core behavior implemented:
  - validated config model and URL normalization
  - auth token acquisition + cache + single-flight lock
  - transport wrapper with auth injection and idempotent-only retry policy
  - centralized sensitive-data redaction in error contexts
- Phase 2 test baseline added:
  - `python/tests/test_config_and_redaction.py`
  - `python/tests/test_auth_provider.py`
  - `python/tests/test_transport.py`
- Phase 2 validation result:
  - Python tests: `7 passed`
  - Lint diagnostics: no issues in `python/src` and `python/tests`
- Phase 2 exit status: **completed**

## Phase 3 - raw endpoint clients (selected v1 scope)

Implement endpoint-parity modules for the selected 61-route v1 scope in Python, using generated inputs where practical and hand-written wrappers where needed:

- authentication and token routes
- users routes
- roles routes
- groups routes
- clients routes
- identity provider routes
- realm config routes

Deliverable: raw route methods for selected v1 routes with typed request/response models and coverage tests.

Priority inclusion (newly added role inheritance routes):

- `POST /admin/realms/{realm}/groups/{group_id}/role-mappings/realm`
- `GET /admin/realms/{realm}/groups/{group_id}/role-mappings/realm`
- `DELETE /admin/realms/{realm}/groups/{group_id}/role-mappings/realm`

### Phase 3A - v2+ full coverage expansion (future)

After v1 stabilization, expand from selected routes to full inventory coverage using `docs/ROUTE_INVENTORY.md`.

Expansion targets include:

- protocol mappers
- scope mappings (beyond v1 subset)
- events and audit expansion
- authentication management full surface
- attack detection and other advanced admin families

### Phase 3 completion record

- Implemented concrete raw methods for all selected families:
  - `raw/auth.py`, `raw/users.py`, `raw/roles.py`, `raw/groups.py`, `raw/clients.py`, `raw/identity_providers.py`, `raw/realms.py`
- Added family route tests:
  - `python/tests/test_raw_auth.py`
  - `python/tests/test_raw_users.py`
  - `python/tests/test_raw_roles.py`
  - `python/tests/test_raw_groups.py`
  - `python/tests/test_raw_clients.py`
  - `python/tests/test_raw_identity_providers.py`
  - `python/tests/test_raw_realms.py`
- Explicitly included group role inheritance routes:
  - `POST /admin/realms/{realm}/groups/{group_id}/role-mappings/realm`
  - `GET /admin/realms/{realm}/groups/{group_id}/role-mappings/realm`
  - `DELETE /admin/realms/{realm}/groups/{group_id}/role-mappings/realm`
- Phase 3 validation result:
  - Selected routes in source list: `61`
  - Implemented route specs: `61`
  - Missing method reachability via `KeycloakClient`: `0`
  - Full Python tests: `14 passed`
  - Lint diagnostics: no issues in `python/src` and `python/tests`
- Phase 3 exit status: **completed**

## Phase 4 - high-level service methods

Build developer-friendly orchestrations on top of raw routes:

- create user + credentials + role mapping + group assignment
- client provisioning and mapper setup workflows
- realm bootstrap helpers for approved scenarios
- session inheritance orchestration (parent authentication -> child silent handoff -> child local session establishment)

Deliverable: service modules with deterministic behavior and clear permission assumptions.

### Phase 4 completion record

- Implemented service layer modules:
  - `python/src/keycloak_client/services/workflow_common.py`
  - `python/src/keycloak_client/services/realm_service.py`
  - `python/src/keycloak_client/services/client_service.py`
  - `python/src/keycloak_client/services/user_service.py`
  - `python/src/keycloak_client/services/group_service.py`
  - `python/src/keycloak_client/services/authorization_service.py`
  - `python/src/keycloak_client/services/inheritance_service.py`
  - `python/src/keycloak_client/services/observability.py`
  - `python/src/keycloak_client/services/problem_details.py`
- Implemented typed workflow models in:
  - `python/src/keycloak_client/models/service_models.py`
- Client integration updated:
  - `python/src/keycloak_client/client.py` now exposes `client.services.*` via `ServiceRegistry`.
- Added Phase 4 test coverage:
  - `python/tests/test_service_realm.py`
  - `python/tests/test_service_client.py`
  - `python/tests/test_service_user.py`
  - `python/tests/test_service_group.py`
  - `python/tests/test_service_authorization.py`
  - `python/tests/test_service_inheritance.py`
  - `python/tests/test_problem_details.py`
  - `python/tests/test_observability.py`
- Validation result:
  - full Python tests: `24 passed`
  - lint diagnostics: no issues in `python/src` and `python/tests`
- Phase 4 exit status: **completed**

### Phase 4A - session inheritance track (cross-realm)

Implement cross-realm session inheritance as a first-class service module in both language SDKs.

Scope and behavior:

- Inheritance model: trusted auth handoff, not shared physical session objects.
- Parent realm authentication can be reused by authorized child realms.
- Child realm must independently validate trust, entitlement, and policy before creating local session.
- Child realms may enforce stricter policy than parent realms (step-up, shorter TTLs, stronger checks).
- Fail closed when trust validation or policy checks fail.

Required route/capability dependencies:

- `GET /realms/{realm}/protocol/openid-connect/auth`
  - required for browser-based and silent handoff (`prompt=none`) flows.
- `POST /realms/{realm}/protocol/openid-connect/token`
  - required for code-to-token exchange, refresh token, and optional token-exchange profile.
- Existing session/logout and role-mapping routes for realm-local control and entitlement checks.

Service-layer outputs:

- `attemptChildSessionInheritance(...)` style operation that:
  1. initiates child realm auth handoff (`/auth`, silent where possible),
  2. validates child realm authorization/entitlement,
  3. creates child local session only on successful checks,
  4. returns typed inheritance outcome (success, policy-required-login, denied).
- `propagateParentLogout(...)` helper:
  - parent session termination immediate,
  - child realm termination best-effort,
  - strict child token/session expiry as fallback control.

Testing additions:

- Silent handoff success/failure tests (`prompt=none`).
- Explicit child entitlement enforcement tests (inheritance does not imply authorization).
- Parent logout propagation behavior tests with delay/failure simulation.
- Multi-level inheritance tests requiring per-hop re-validation.

## Phase 5 - BFF compatibility module

Preserve and isolate BFF workflow support:

- `buildLoginUrl`
- `completeLogin`
- `refresh`
- `logout`
- `getUserInfo`

Keep this API separated from direct admin modules so consumers can adopt only the needed surface.

Deliverable: BFF module aligned with `KEYCLOAK_BFF_CLIENT_REPO_HANDOFF.md`.

### Phase 5 completion record

- BFF compatibility module implemented and covered:
  - `python/src/keycloak_client/services/bff_compatibility.py`
  - tests in `python/tests/test_bff_compatibility.py`
- Regression and security evidence captured in:
  - `docs/PHASE_5_EXIT_EVIDENCE.md`
- CI/release baseline in place from Phase 5:
  - `.github/workflows/python-ci-release.yml` (build + tag-gated private publish)
- Compatibility and operations documentation linked:
  - `docs/KEYCLOAK_COMPATIBILITY_POLICY.md`
  - `docs/SERVICE_USAGE.md`
  - `docs/OPERATIONS_RUNBOOK.md`
- Phase 5 exit status: **completed**

### Phase 5A - TypeScript rollout plan

- Frontend-safe auth helper package/surface first (no admin credentials, no `/admin/*` routes).
- Backend TypeScript admin mirror begins only after Python API and security behavior are stable.

## Phase 6 - security hardening and compliance checks

1. Add redaction test suite to prove token/secret/PII are never emitted.
2. Add auth-race tests for token refresh concurrency.
3. Validate retry behavior only for safe/idempotent operations by default.
4. Document least-privilege role model per route family.
5. Add dangerous-operation safeguards and docs warnings.
6. Add inheritance-specific controls:
   - mandatory child entitlement checks,
   - explicit no-implicit-transitive-trust rule,
   - high-risk operation step-up recommendation under inherited sessions,
   - strict child lifetime bounds for logout propagation gaps.

Deliverable: `docs/SECURITY_MODEL.md` + passing security-focused tests.

### Phase 6 completion record

- Expanded redaction and BFF observability tests: `python/tests/test_security_redaction.py`, `python/tests/test_bff_compatibility.py`.
- Transport retry and 403 least-privilege tests: `python/tests/test_transport.py`.
- Auth provider single-flight documentation and stronger concurrency sample: `python/src/keycloak_client/auth_provider.py`, `python/tests/test_auth_provider.py`.
- Least-privilege matrix: `docs/KEYCLOAK_LEAST_PRIVILEGE.md`; `docs/SECURITY_MODEL.md` updated (typo fix, inheritance section §9, transport retry clarification, dangerous-ops gate).
- Dangerous operations: `KeycloakClientConfig.allow_dangerous_operations`, `python/src/keycloak_client/dangerous_ops.py`, `KeycloakClient.dangerous_realm_logout_all`, realm bootstrap compensation requires the flag; tests in `python/tests/test_dangerous_ops.py`, `python/tests/test_service_realm.py`.
- Inheritance edge tests: `python/tests/test_security_inheritance.py`.
- Validation: `pytest` (full `python/tests/`) green.

## Phase 7 - integration, compatibility, and CI

1. Add integration tests against containerized Keycloak for v1 route families.
2. Add CI matrix:
   - Python lint, typing, unit/integration tests
   - TypeScript lint, typecheck, unit/integration tests
3. Add OpenAPI drift checks for supported Keycloak versions.
4. Define upgrade workflow when Keycloak introduces API changes.

Deliverable: CI-proven compatibility baseline and drift detection.

### Phase 7 completion record

- **CI:** `.github/workflows/python-ci-release.yml` runs **quality** (Ruff, Mypy, unit tests, build), **openapi-drift** (`scripts/check_keycloak_openapi_drift.py` against Admin OpenAPI), and **integration-keycloak** (Docker Keycloak `26.0.7`, `KEYCLOAK_INTEGRATION=1`, `pytest tests/integration`). Tag publish gates on all three jobs.
- **Python tooling:** `ruff` and `mypy` in `python/pyproject.toml` optional dev extra; line length 100; pragmatic mypy (`disallow_untyped_defs` off, `check_untyped_defs` on).
- **Docs:** `docs/OPENAPI_DRIFT.md`, `docs/KEYCLOAK_UPGRADE_WORKFLOW.md`; `docs/INTEGRATION_TESTING.md` and `docs/KEYCLOAK_COMPATIBILITY_POLICY.md` updated for CI and upgrade flow.
- **Local integration compose:** `python/tests/integration/docker-compose.keycloak.yml` image aligned with CI (`26.0.7`, dev HTTP flags).
- **TypeScript CI matrix:** **Deferred** until a `typescript/` package exists in this repository; Phase 7 implements Python-first gates only.

## Phase 8 - documentation and release readiness

1. Root README:
   - architecture
   - quick-start examples
   - module boundaries (admin vs BFF vs inheritance services)
2. Language package READMEs:
   - installation
   - auth configuration
   - common tasks
   - session inheritance flow examples and caveats
3. Publish route-to-method mapping and permission notes.
4. Finalize release pipeline for PyPI and npm.
5. Finalize private registry publishing workflow and consumer setup docs:
   - pip private index configuration
   - npm private registry configuration
   - internal authentication/token setup guidance

Deliverable: publish-ready docs and release workflow.

### Phase 8 completion record

- Root README expanded with architecture, quick-start, and module boundaries:
  - `README.md`
- Language package docs:
  - `python/README.md` (install/auth/common tasks/session inheritance notes)
  - TypeScript package README/publish docs remain deferred until `typescript/` package exists
- Route mapping and permission publication:
  - `docs/ROUTE_METHOD_PERMISSION_MAP.md`
- Release workflow documentation finalized:
  - `docs/RELEASE_PROCESS.md`
  - `docs/RELEASE_PIPELINES.md`
  - `scripts/pre_release_validation.sh` as local release gate helper
- Consumer private registry setup docs:
  - `docs/PRIVATE_REGISTRY_CONSUMER_SETUP.md` (pip + npm guidance, npm marked deferred)
- Phase 8 status: **completed for Python-first scope** (TypeScript package/pipeline pending package creation).

## Testing matrix (minimum)

| Area | Python | TypeScript |
|------|--------|------------|
| Transport/auth/error primitives | pytest | vitest/jest |
| Endpoint path/query/header/body correctness | pytest | vitest/jest |
| Error mapping (401/403/404/409/429/5xx) | pytest | vitest/jest |
| Token refresh race handling | pytest | vitest/jest |
| Sensitive-data redaction | pytest | vitest/jest |
| Cross-realm inheritance (`/auth` silent handoff + entitlement) | pytest | vitest/jest |
| Integration on containerized Keycloak | pytest | vitest/jest |

## Open questions to close before coding phase starts

- Code generation workflow policy:
  - Commit generated raw bindings to repository for reproducible builds.
  - Regenerate in CI on explicit upgrade workflows and fail on diff drift.

## Scope consistency note

- `docs/ROUTE_INVENTORY.md` remains the complete reference map (387 operations) for long-term coverage.
- `docs/SELECTED_ROUTES_AND_USE_CASES.md` is the implementation source-of-truth for v1 execution (61 routes).

## References

- [`KEYCLOAK_CLIENT_LIBRARY_REQUIREMENTS.md`](./KEYCLOAK_CLIENT_LIBRARY_REQUIREMENTS.md)
- [`KEYCLOAK_BFF_CLIENT_REPO_HANDOFF.md`](../KEYCLOAK_BFF_CLIENT_REPO_HANDOFF.md)
- [`SELECTED_ROUTES_AND_USE_CASES.md`](./SELECTED_ROUTES_AND_USE_CASES.md)
- [Keycloak Admin REST API](https://www.keycloak.org/docs-api/latest/rest-api/index.html)
- [RFC 9700 OAuth 2.0 Security BCP](https://datatracker.ietf.org/doc/rfc9700/)

## Phase 0 completion checklist

- Package names and runtime baselines are explicitly locked.
- Cross-route security model is documented and referenced.
- Release/versioning policy is documented with breaking-change rules.
- No unresolved Phase 0 blockers remain before Phase 1 route inventory.

## Transition gate to Phase 1

Phase 1 can start only when all conditions below are true:

1. `docs/KEYCLOAK_CLIENT_LIBRARY_REQUIREMENTS.md` includes locked defaults and compatibility policy.
2. `docs/SECURITY_MODEL.md` is present and approved as baseline for all SDK modules.
3. `docs/IMPLEMENTATION_PLAN.md` includes locked decision table and release policy.
4. No open question remains that changes route inventory structure or auth/transport architecture.
