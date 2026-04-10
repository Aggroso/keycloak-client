# Consumer integration requirements

This document is the **integrator contract**: what the SDK provides, what your application must own, and a minimal **happy path** to go live.

## Library vs app-owned

| Responsibility | Owner |
|----------------|--------|
| Keycloak Admin REST and selected OIDC endpoints, transport, retries, redaction | **SDK** |
| Optional BFF helpers (build login URL, code exchange, refresh, logout call, userinfo) | **SDK** (mechanics only) |
| Idempotent provisioning helpers (`ensure_realm`, `ensure_client_by_client_id`, …) | **SDK** |
| PKCE verifier generation, **`state` / `nonce` storage**, and redirect/callback validation policy | **App** |
| **Redirect URI allow-list policy** and per-tenant/client routing | **App** |
| **Local DB** user/tenant sync and mapping Keycloak `sub` to your domain model | **App** |
| **App-issued JWTs**, cookies, and **session lifecycle** outside Keycloak APIs | **App** |
| **Logout cleanup** (clear app cookies, revoke app sessions, device UX) beyond calling Keycloak logout | **App** |
| Threat model for cross-realm flows, Keycloak realm/client configuration | **App** + **SDK docs** (`SESSION_INHERITANCE.md`) |

The SDK does **not** provide: PKCE/state storage, redirect URI policy, local DB user/tenant sync, app-issued JWT/sessions, or logout cleanup—only the Keycloak-facing HTTP and optional helpers.

## Happy path integrator story

1. **Python 3.11+** on the server image (`python3.11 -m pip …`).
2. **Install** a tagged revision (replace with the latest release tag):

   ```bash
   python3.11 -m pip install "git+https://github.com/Aggroso/keycloak-client.git@v0.1.2#subdirectory=python"
   ```

3. **Dual URL**: set `base_url` to the **internal** Keycloak base (e.g. `http://keycloak:8080`) for Admin API, token, and server-side OIDC calls. Set `public_base_url` to the **browser-facing** URL (e.g. `https://auth.example.com`) so `services.bff.build_login_url` emits links users can open.
4. **Admin authentication** (pick one):
   - Default: **client credentials** (`client_id` + `client_secret`, service account).
   - **Password grant** (ROPC): `token_endpoint_grant="password"` plus `resource_owner_username` / `resource_owner_password` on `KeycloakClientConfig`—see security warnings in README; prefer service accounts in production.
   - **Injected Bearer**: `KeycloakClient(config, access_token_provider=your_async_callable)` so Admin calls use your token (e.g. password-grant token from elsewhere) with **single-flight** caching left to your provider unless you use `AuthProvider`.
5. **OIDC auth-code**: register a confidential client; use BFF helpers to build the authorize URL (your app still stores `state`/`nonce` and validates the callback). Exchange the code server-side with `complete_login`.
6. **Provisioning**: use `keycloak_client.ensure_realm`, `ensure_client_by_client_id`, `ensure_realm_role`, `ensure_user_by_username`, `ensure_protocol_mapper` in bootstrap jobs instead of ad-hoc scripts.
7. **Sync code**: from a blocking context, use `keycloak_client.sync_support.run_async(your_coro)` only for scripts/CLIs—not from inside a running asyncio loop.

## Capabilities (status)

| Capability | Status |
|-------------|--------|
| Pluggable Admin Bearer via `access_token_provider` on `KeycloakClient` | Implemented |
| Password grant on `AuthProvider` + `fetch_resource_owner_password_token` helper | Implemented (discouraged for interactive users) |
| `public_base_url` for BFF authorize URL | Implemented |
| Idempotent `ensure_*` provisioning helpers | Implemented |
| `sync_support.run_async` for scripts | Implemented |
| Cross-realm trust handoff documentation | `docs/SESSION_INHERITANCE.md` |

## Optional / backlog

- **Custom TLS / CA bundle**, HTTP(S) proxy on `httpx` client
- **Keycloak version matrix** in CI/docs
- Richer **sync** façade (beyond `run_async`)

## References

- [`SESSION_INHERITANCE.md`](./SESSION_INHERITANCE.md) — threat model and parent→child reference flow
- Root [`README.md`](../README.md) — install lines and “what this library does not do”
