# Cross-realm session inheritance (trust handoff)

The SDK exposes `InheritanceService` as **optional building blocks** for patterns where a user
already has a session in a **parent** realm and you want a controlled transition to a **child**
realm. This is **not** a shared session object, a shared refresh token across realms, or
automatic propagation of browser cookies. It is a **trust handoff**: your app and Keycloak
configuration must enforce who may obtain tokens in the child realm and how.

## Threat model (summary)

| Concern | Implication |
|--------|-------------|
| Cross-realm token theft | Child-realm tokens must only be issued to the intended subject; never skip child-realm authorization checks. |
| Confused deputy | The child realm must not treat “parent realm said OK” as sufficient unless you implement explicit policy (roles, groups, IdP links). |
| Silent SSO abuse | `prompt=none` can succeed when a browser already has a Keycloak session; combine with short TTLs, step-up auth, and app-level checks for sensitive actions. |
| Logout inconsistency | Logging out the parent realm does not guarantee child sessions end; plan TTL, back-channel logout, or admin user logout where appropriate. |

## Required Keycloak configuration (conceptual)

Exact steps depend on your Keycloak version and topology. In general:

1. **Realms**: Distinct parent and child realms (or shared realm with different clients—adjust the model accordingly).
2. **Clients**: Each realm has OIDC clients with correct redirect URIs, PKCE where used, and token lifetimes aligned with your risk tolerance.
3. **User identity**: Same person in parent and child is usually **same username with a linked account**, **federated IdP**, or **user federation**—not an automatic assumption the SDK can make.
4. **Child entitlement**: Before treating inheritance as successful, enforce **child-realm roles or groups** (the service includes a placeholder role-mapping read for this reason).

## Minimal reference flow (parent → child)

1. User completes login in the **parent** realm (authorization code + PKCE in your BFF is typical).
2. Your backend needs access in the **child** realm:
   - Option A: Use **admin APIs** with a service account to provision or inspect the user in the child realm, then issue app-specific authorization.
   - Option B: Attempt **silent SSO** in the child realm (`prompt=none`) in the browser so Keycloak can establish a child session **if** a shared SSO cookie exists and policy allows.
3. Call `InheritanceService.attempt_child_session_inheritance` only as a **starting point**: it combines a silent auth probe, child role mapping read, and a token call shape that may require you to pass real `refresh_token` / parameters in production code paths.
4. On parent logout, `propagate_parent_logout` illustrates calling parent logout and best-effort child user logout; **your app** still owns cookie clearing, app session revocation, and device semantics.

For code entrypoints, see `python/src/keycloak_client/services/inheritance_service.py` and service tests under `python/tests/`.

## SDK scope

- The SDK does **not** store PKCE `state`/`nonce`, manage redirect URI policy, or implement tenant DB sync.
- The SDK does **not** replace Keycloak’s session store or guarantee cross-realm single logout without your configuration.

See also [`CONSUMER_INTEGRATION_REQUIREMENTS.md`](./CONSUMER_INTEGRATION_REQUIREMENTS.md) and [`SECURITY_MODEL.md`](./SECURITY_MODEL.md).
