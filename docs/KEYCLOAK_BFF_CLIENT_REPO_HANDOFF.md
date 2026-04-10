# Keycloak BFF client — handoff for a **separate repository**

Copy this file into the new repo (e.g. `docs/CONTEXT.md` or `README.md` appendix) or attach it in Cursor when opening that workspace. It gathers what multi-app clients must implement against **Planar’s auth BFF** (or any compatible server).

**Related (this monorepo):** normative BFF behavior and security notes — [KEYCLOAK_CLIENT_REQUIREMENTS.md](./KEYCLOAK_CLIENT_REQUIREMENTS.md).  
**Reference implementation:** `backend/app/routes/keycloak_auth.py`, `backend/app/services/keycloak_auth.py` (do **not** import from Planar in the client repo).

---

## Purpose of the new repository

Deliver **reusable client libraries** (Python + TypeScript) so many applications can integrate **Keycloak-backed login** by calling **only your HTTP API** (backend-for-frontend). Applications do **not** call Keycloak’s OIDC endpoints directly.

---

## Suggested naming

- **Repository:** `keycloak-bff-client` (or `yourorg/keycloak-bff-client`)
- **PyPI:** `keycloak-bff-client` or `yourorg-keycloak-bff-client`
- **npm:** `@yourorg/keycloak-bff-client`

**Short description (≤350 characters):**

`Python & TypeScript clients for Keycloak SSO via your OIDC BFF: login URL, callback, refresh, logout. Apps call your API only—not Keycloak. Reuse across many services.`

---

## What the client **is** / **is not**

| Is | Is not |
|----|--------|
| Thin wrapper over **your** REST routes | Keycloak Admin REST client |
| Builds login URLs, calls callback/refresh/logout/userinfo | Full OIDC library inside the browser for token endpoints |
| Configurable `baseUrl` + optional path prefix | Coupled to the Planar codebase |

---

## BFF HTTP contract (default prefix)

Prefix is configurable; **Planar default** is `/auth/keycloak`.

| Method | Path | Role |
|--------|------|------|
| GET | `{prefix}/login` | Start OIDC (PKCE, state, nonce on server). Query: `redirect_uri` (optional), `prompt` (optional). **Response:** `302` to Keycloak. |
| GET | `{prefix}/callback` | Finish OIDC. Query: `code`, `state`; optional `error`, `error_description`. **Success:** JSON (see below). |
| POST | `{prefix}/refresh` | Body JSON: `{ "refresh_token": "<string>" }`. Returns new tokens. |
| POST | `{prefix}/logout` | Header: `Authorization: Bearer <access_token>`. Body JSON (optional): `redirect_uri`, `id_token_hint`. Returns JSON including `logout_url`. |
| GET | `{prefix}/logout` | Redirect-style logout; POST preferred when bearer is available. |
| GET | `{prefix}/userinfo` | Header: `Authorization: Bearer <token>`. Returns safe claims subset. |

### Callback success JSON (representative)

Planar issues **app** JWTs after Keycloak exchange; shape includes:

- `access_token`, `refresh_token`, `token_type` (e.g. `bearer`)
- `id_token` — may be present when Keycloak returns it (used for logout hint)
- `user`: `id`, `email`, `full_name`, `role`, `access_role`, `is_super_admin`, `is_primary_admin`, `is_company_admin` (if present), `must_reset_password` (if present)
- `session_id`

**Clients should treat unknown fields as forward-compatible** (extra keys allowed).

### Error handling

- BFF may return `4xx`/`5xx` with JSON `detail` (FastAPI style). Map to typed errors in each language; **never log** access or refresh tokens.

---

## Library design (both languages)

### Configuration

- `baseUrl` — origin only, e.g. `https://api.example.com` (no trailing slash)
- `authPathPrefix` — default `/auth/keycloak`
- `timeout` / `fetch` options as idiomatic for each runtime

### Public API (conceptual)

1. `buildLoginUrl(redirectUri?, prompt?)` → string (full URL to open in browser or return as `RedirectResponse`)
2. `completeLogin(code, state)` → typed result (HTTP GET callback)
3. `refresh(refreshToken)` → typed result
4. `logout(accessToken, { redirectUri?, idTokenHint? })` → `{ logout_url, ... }`
5. `getUserInfo(accessToken)` → claims object (optional)

Use **native types** (Pydantic v2 / Zod / TypeScript interfaces) matching the JSON above.

### Security notes for consumers

- **Do not** ship Keycloak **client secrets** in browser bundles.
- Prefer **BFF + HttpOnly session** long term; if the BFF returns bearer tokens to the SPA, document XSS and storage risk (see requirements doc Tier 1 vs Tier 2).

---

## Repository layout (suggestion)

```
keycloak-bff-client/
  README.md
  LICENSE
  docs/
    BFF_CONTRACT.md          # optional duplicate of this contract
  python/
    pyproject.toml
    src/keycloak_bff_client/  # or oidc_bff_client — pick one package name
  typescript/
    package.json
    src/index.ts
```

Alternatively a **single** `packages/python` and `packages/typescript` tree under one repo.

---

## Tests (minimum)

- **Unit:** mock HTTP; assert correct paths, query strings, headers, JSON bodies; no live Keycloak.
- **Contract:** when Planar exposes OpenAPI for `/auth/keycloak/*`, add optional schema validation or snapshot tests.

---

## Cursor / AI starter prompt (paste in the **new** repo)

```text
Implement keycloak-bff-client in this repository using docs/KEYCLOAK_BFF_CLIENT_REPO_HANDOFF.md (or CONTEXT.md).

Deliver:
1. Python package: httpx async client, Pydantic models, KeycloakBffClient class with build_login_url, complete_login, refresh, logout, get_userinfo.
2. TypeScript package: fetch-based client, same methods, ESM + types.
3. README with install, config, and browser vs server usage notes.
4. pytest and vitest/jest tests with mocked HTTP.

No dependency on Planar; default prefix /auth/keycloak; configurable baseUrl.
```

---

## Changelog in Planar

When the external repo is published, add its URL to this project’s README or deployment docs so integrators know where to install the client.

---

*This handoff is maintained in Planar for continuity; the canonical client source of truth lives in the dedicated repository once created.*
