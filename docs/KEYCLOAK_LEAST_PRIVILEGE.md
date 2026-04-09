# Keycloak least privilege (v1 SDK)

This is a **starting point** for assigning Keycloak permissions to the confidential client used by `keycloak-client`. Verify against your Keycloak version and org policy.

## References

- Selected routes: [SELECTED_ROUTES_AND_USE_CASES.md](./SELECTED_ROUTES_AND_USE_CASES.md)
- Full inventory: [ROUTE_INVENTORY.md](./ROUTE_INVENTORY.md)
- Security baseline: [SECURITY_MODEL.md](./SECURITY_MODEL.md)

## Route families and typical admin roles

| Family | Example operations | Typical realm-management roles / notes |
|--------|--------------------|----------------------------------------|
| OIDC runtime | token, logout, userinfo, discovery, JWKS, `/auth` | Usually **no** admin token; end-user or public client flows. Admin client used only for server-side token exchange patterns you control. |
| Realm admin | create/update realm, keys, `logout-all` | `realm-admin` or fine-grained `manage-realm`, `manage-users`, `manage-clients` as needed. **`logout-all` is high impact** — treat as dangerous (see [SECURITY_MODEL.md](./SECURITY_MODEL.md)). |
| Users | CRUD, reset-password, sessions, logout user, credentials | `manage-users` (or composite `realm-admin`). |
| Roles | realm roles, user/group role mappings | `manage-realm` / role-mapping permissions. |
| Groups | CRUD, members, path lookup | `manage-users` + group permissions depending on Keycloak version. |
| Clients | CRUD, client-secret read/rotate | `manage-clients`. **Secret rotation is high risk.** |
| Identity providers | CRUD, import-config | `manage-identity-providers`. |
| Auth admin extras | `client-session-stats`, realm `keys` | `view-realm` / `manage-realm` as appropriate. |

## Confidential client used for Admin REST

- Prefer a **dedicated** service account with **only** the composite roles needed for the route families you call.
- Never reuse the same client for browser public flows and admin operations.

## Dangerous operations (v1 selected routes)

High-impact endpoints to gate in application design (SDK provides `allow_dangerous_operations` for selected workflows; raw routes are otherwise unrestricted):

| Area | Route / operation | Risk |
|------|-------------------|------|
| Sessions | `POST /admin/realms/{realm}/logout-all` | Logs out **all** users in the realm. |
| Users | `DELETE /admin/realms/{realm}/users/{id}` | Permanent user deletion. |
| Clients | `POST .../client-secret` | Secret rotation breaks existing integrations until updated. |
| Clients | `DELETE /admin/realms/{realm}/clients/{id}` | Removes client configuration. |
| Realms | `DELETE /admin/realms/{realm}` (compensation rollback) | Destroys realm; gated via `allow_dangerous_operations` when used from `bootstrap_realm` rollback. |
| Roles / groups / IdPs | Deletes on roles, groups, identity providers | Can break login and authorization paths. |

Use `KeycloakClient.dangerous_realm_logout_all(realm)` instead of calling raw `logout-all` directly so the dangerous flag is enforced.

## 403 forbidden (least privilege)

If the client lacks required roles, Keycloak returns **403**. The SDK surfaces `KeycloakApiError` with `context.status_code == 403` and `retryable=False`. Treat as configuration or authorization failure, not a transport retry case.
