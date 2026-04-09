# Security model: keycloak-client SDKs

This document defines mandatory, consistent security behavior across Python and TypeScript SDKs for all route families.

Per–route-family permission guidance: [KEYCLOAK_LEAST_PRIVILEGE.md](./KEYCLOAK_LEAST_PRIVILEGE.md).

## 1) Security posture

- Admin operations are server-side only.
- Browser-facing usage is limited to safe auth/BFF helpers.
- Confidential credentials are never shipped to browser/mobile bundles.
- All SDK modules follow one shared auth, transport, logging, and error policy.

## 2) Authentication model

- Admin API auth uses confidential client credentials.
- Token provider behavior:
  - cache access token in memory only
  - refresh/acquire before expiration using configurable skew (default: 60s)
  - enforce single-flight refresh lock per credential set
  - fail closed when refresh/acquire fails
- Optional external token injection is allowed for advanced deployments, but still passes through redaction and expiry validation rules.

## 3) Transport policy (all routes)

- HTTPS required by default; insecure HTTP must be explicit opt-in for local development only.
- Timeouts:
  - connect timeout default: 5s
  - request timeout default: 30s
- Retries:
  - default retries only for idempotent methods (`GET`, `HEAD`, `OPTIONS`) on **transport-layer** failures (e.g. connection errors)
  - HTTP 4xx/5xx responses are not automatically retried by the transport loop (fail fast with typed errors)
  - no automatic retries for mutating methods (`POST`, `PUT`, `PATCH`, `DELETE`) on transport failures unless explicitly enabled by caller configuration
- Headers:
  - normalized `Authorization: Bearer <token>`
  - stable user-agent identifying sdk name/version
  - optional trace/correlation header pass-through

## 4) Redaction policy (mandatory)

Never log or expose these values in logs, errors, metrics tags, or traces:

- access tokens
- refresh tokens
- client secrets
- authorization headers
- passwords and credential payloads
- sensitive PII fields where present

Redaction strategy:

- header redaction by key match (`authorization`, `cookie`, `set-cookie`)
- body redaction by key match (`access_token`, `refresh_token`, `client_secret`, `password`, `secret`)
- nested object traversal with max-depth safeguards
- preserve structural context while replacing values with `[REDACTED]`

## 5) Authorization and dangerous operations

- Route inventory must map each route family to minimum required Keycloak permissions/roles (see [KEYCLOAK_LEAST_PRIVILEGE.md](./KEYCLOAK_LEAST_PRIVILEGE.md)).
- Least-privilege defaults are required; avoid blanket admin role assumptions.
- High-risk operations must be explicitly marked in docs and method comments:
  - realm delete/reset
  - client secret rotation
  - bulk delete/update
  - identity provider destructive updates
  - `logout-all` (terminates all sessions in a realm)

Python SDK guardrails:

- `KeycloakClientConfig.allow_dangerous_operations` (default `false`): required for selected high-impact workflows (e.g. `KeycloakClient.dangerous_realm_logout_all`, and realm-delete compensation during `bootstrap_realm` when `allow_destructive_rollback` is enabled).
- Raw route modules under `keycloak_client.raw.*` do **not** enforce this flag; callers must avoid exposing them to untrusted code.

Optional high-risk guardrails (recommended):

- per-operation confirmation callback hook for CLI tooling

## 6) Error model requirements

- Use typed errors with:
  - HTTP status
  - service/operation metadata
  - parsed Keycloak error payload (when available)
  - retryability classification
- Error messages must be redaction-safe by construction.
- TypeScript returns may support result wrappers, but thrown typed errors are the default.

## 7) Compliance baseline

The SDK security design aligns with:

- OAuth 2.0 Security Best Current Practice (RFC 9700)
- Official Keycloak security and adapter guidance
- OWASP API Security Top 10 (2023)

## 8) Security testing requirements

- Unit tests for redaction of headers/body tokens and secrets.
- Token refresh concurrency tests (single-flight guarantees).
- Retry policy tests validating idempotent-only default retries.
- Permission/forbidden-flow tests against containerized Keycloak.
- Regression tests to ensure no new log line leaks redacted keys.

## 9) Cross-realm session inheritance (controls)

- **No implicit transitive trust:** a valid parent-realm session does **not** authorize the child realm. Child access requires explicit child-realm entitlements (e.g. role/group checks).
- **Mandatory child checks:** treat inheritance as **denied** if child entitlement cannot be verified.
- **Logout propagation gaps:** if parent logout succeeds but child session termination fails, applications must enforce **short-lived child tokens/sessions** and re-validation at sensitive actions.
- **High-risk actions:** under inherited or handoff sessions, require **step-up authentication** (full interactive login or stronger assurance) before destructive admin operations or sensitive data access.
