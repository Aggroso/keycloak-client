# Keycloak client library requirements

This document defines requirements for a production-grade `keycloak-client` repository that provides Python and TypeScript libraries for Keycloak integration with comprehensive route coverage and consistent security.

## 0) Phase 0 locked defaults

- v1 scope target: all available Keycloak routes (implemented in phases with explicit inventory coverage).
- Realm creation support: included in v1 runtime methods as high-risk operations.
- Error behavior: support typed exceptions and result wrappers; default to typed exceptions.
- Keycloak compatibility target for v1: latest stable release only.
- Python package baseline: package `keycloak_client`, Python 3.11+.
- TypeScript package baseline: package `@yourorg/keycloak-client`, Node 20 LTS+.
- Versioning baseline: independent semver per language package, with aligned release notes/changelog policy.

## 1) Product scope

- Provide a reusable client library that maps Keycloak capabilities to typed methods.
- Support both:
  - **Auth/BFF integration** (existing handoff use case: login, callback, refresh, logout, userinfo through your API).
  - **Keycloak Admin API integration** (realm-scoped administration from trusted backend code).
- Keep coverage aligned with Keycloak API evolution using official docs/OpenAPI as source-of-truth.

## 2) Supported clients and environments

- **Python package** for backend services and workers.
- **TypeScript package** for Node.js backend services and tools.
- Browser usage is allowed only for explicitly safe auth helpers; admin operations are server-only.

## 3) Functional requirements

### 3.1 Route mapping requirements

- Every supported Keycloak route group must map to typed methods in both language SDKs.
- Route mapping must be traceable with a route inventory table:
  - endpoint path
  - HTTP method
  - service/module name
  - method name
  - request/response model
- Route families to cover (phased):
  - Realms
  - Users
  - Groups
  - Roles (realm and client)
  - Clients and protocol mappers
  - Identity providers
  - Authentication and required actions
  - Sessions and events
  - Attack detection
  - Token/OIDC operations relevant to backend usage

### 3.2 API shape requirements

- Expose two layers:
  - **Raw API layer**: close to endpoint parity.
  - **Service layer**: higher-level workflows composed from raw endpoints.
- Use strongly typed request/response models:
  - Python: Pydantic v2 models or equivalent typed models.
  - TypeScript: interfaces/types and optional runtime validators.
- Preserve forward compatibility for unknown fields where Keycloak may add fields.

### 3.3 BFF compatibility requirements

- Maintain compatibility with the BFF contract in `KEYCLOAK_BFF_CLIENT_REPO_HANDOFF.md`.
- Keep BFF-facing methods logically separate from direct Keycloak Admin methods.

## 4) Security requirements (mandatory and consistent)

### 4.1 Authentication and secrets

- Admin routes must use confidential client authentication (service account), never browser-exposed secrets.
- Centralized token provider with:
  - short-lived cached access token
  - refresh/acquire before expiry with configurable skew
  - concurrency-safe refresh (single-flight lock)
- Do not log secrets, tokens, passwords, authorization headers, or sensitive PII fields.

### 4.2 Transport and request policy

- HTTPS/TLS required for production usage.
- Centralized HTTP policy across all routes:
  - timeouts
  - retry strategy (idempotent-safe by default)
  - request/response size constraints where practical
  - standardized user-agent and trace headers (optional)
- Apply the same sanitization and error policy to all services/modules.

### 4.3 Authorization and least privilege

- Document required Keycloak roles/scopes per route family.
- Encourage least privilege role assignment; avoid requiring blanket realm-admin for all operations.
- Mark dangerous operations (realm/client deletion, secret rotation, bulk destructive updates) with explicit warnings in docs.

### 4.4 Standards baseline

- Security posture must align with:
  - OAuth 2.0 Security BCP (RFC 9700)
  - Keycloak official security guidance
  - OWASP API Security Top 10 (for API misuse and access-control risks)

## 5) Reliability and error-handling requirements

- One consistent SDK error model per language that includes:
  - HTTP status
  - parsed Keycloak error payload when available
  - retryability classification
  - operation context metadata (service/endpoint)
- Define deterministic behavior for:
  - 401/403/404/409/422/429/5xx responses
  - pagination and cursor/offset params
  - partial update semantics

## 6) Compatibility and versioning requirements

- Declare supported Keycloak major/minor versions.
- Run compatibility tests against supported versions.
- Detect and track API drift on Keycloak upgrades via OpenAPI diff/contract checks.
- Version SDKs with semver and document breaking-change policy.
- Maintain explicit upgrade notes for each Keycloak version bump, including route/model diffs.

## 7) Testing requirements

- Unit tests:
  - request construction (path, query, headers, body)
  - response parsing
  - error mapping
- Integration tests:
  - containerized Keycloak for core route families
  - auth lifecycle and permission boundary checks
- Security tests:
  - redaction tests
  - token refresh race/concurrency tests
  - forbidden access and least-privilege behavior

## 8) Documentation requirements

- Provide:
  - architecture overview
  - route-to-method mapping table
  - security model and deployment guidance
  - per-method examples
  - migration/version compatibility notes

## 9) Non-goals

- No frontend-embedded admin credentials or direct browser admin operations.
- No coupling to Planar code internals.
- No promise of day-one support for every possible extension endpoint without phased rollout.

## 10) Reference baseline (for implementation decisions)

- Keycloak Admin REST API docs and OpenAPI definitions.
- `@keycloak/keycloak-admin-client` (official Node admin client) for coverage and ergonomics references.
- `python-keycloak` for Python API design and ecosystem expectations.
- `openid-client` patterns for robust OAuth/OIDC token handling in Node-side integrations.
