# Selected Keycloak routes and use cases (strict core set)

This is the trimmed core route set aligned to your latest instruction: keep only required routes, remove non-included extras, and stay below 65 routes.

## 1) Authentication and token (routes 1-10, 10 routes)

| Method | Route | Why we use it |
|---|---|---|
| `POST` | `/realms/{realm}/protocol/openid-connect/token` | Token exchange and refresh (`grant_type` driven, including `refresh_token` and optional token-exchange profile). |
| `POST` | `/realms/{realm}/protocol/openid-connect/logout` | RP-initiated logout. |
| `GET` | `/realms/{realm}/protocol/openid-connect/userinfo` | Fetch authenticated user claims. |
| `GET` | `/realms/{realm}/protocol/openid-connect/certs` | JWKS for token signature validation. |
| `GET` | `/realms/{realm}/.well-known/openid-configuration` | OIDC discovery metadata. |
| `GET` | `/realms/{realm}/protocol/openid-connect/auth` | Browser login/authorization start; required for silent child-realm handoff (`prompt=none`) in session inheritance flows. |
| `POST` | `/realms/master/protocol/openid-connect/token` | Admin/bootstrap token acquisition. |
| `POST` | `/admin/realms/{realm}/logout-all` | Force logout all user sessions in realm. |
| `GET` | `/admin/realms/{realm}/client-session-stats` | Client session metrics. |
| `GET` | `/admin/realms/{realm}/keys` | Realm key inspection. |

## 2) User CRUD and lifecycle (routes 11-24, 14 routes)

| Method | Route | Why we use it |
|---|---|---|
| `GET` | `/admin/realms/{realm}/users` | List/search users. |
| `POST` | `/admin/realms/{realm}/users` | Create user. |
| `GET` | `/admin/realms/{realm}/users/{user_id}` | Get user details. |
| `PUT` | `/admin/realms/{realm}/users/{user_id}` | Update user profile/state. |
| `DELETE` | `/admin/realms/{realm}/users/{user_id}` | Delete user. |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/reset-password` | Admin password reset/change. |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/send-verify-email` | Trigger verify-email mail. |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/execute-actions-email` | Trigger required actions (verify/update-password/etc). |
| `GET` | `/admin/realms/{realm}/users/{user_id}/credentials` | List user credentials. |
| `DELETE` | `/admin/realms/{realm}/users/{user_id}/credentials/{credentialId}` | Remove a user credential. |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/disable-credential-types` | Disable selected credential types. |
| `GET` | `/admin/realms/{realm}/users/{user_id}/sessions` | List user sessions. |
| `POST` | `/admin/realms/{realm}/users/{user_id}/logout` | Logout specific user sessions. |
| `GET` | `/admin/realms/{realm}/users/{user_id}/consents` | Inspect user consent grants. |

## 3) Role management (routes 25-35, 11 routes)

| Method | Route | Why we use it |
|---|---|---|
| `GET` | `/admin/realms/{realm}/roles` | List realm roles. |
| `POST` | `/admin/realms/{realm}/roles` | Create realm role. |
| `GET` | `/admin/realms/{realm}/roles/{role_name}` | Get role details. |
| `PUT` | `/admin/realms/{realm}/roles/{role_name}` | Update role. |
| `DELETE` | `/admin/realms/{realm}/roles/{role_name}` | Delete role. |
| `GET` | `/admin/realms/{realm}/users/{user_id}/role-mappings/realm` | List user realm-role mappings. |
| `POST` | `/admin/realms/{realm}/users/{user_id}/role-mappings/realm` | Assign realm roles to user. |
| `DELETE` | `/admin/realms/{realm}/users/{user_id}/role-mappings/realm` | Remove realm roles from user. |
| `POST` | `/admin/realms/{realm}/groups/{group_id}/role-mappings/realm` | Assign realm roles to group (members inherit roles automatically). |
| `GET` | `/admin/realms/{realm}/groups/{group_id}/role-mappings/realm` | Get realm roles assigned to group. |
| `DELETE` | `/admin/realms/{realm}/groups/{group_id}/role-mappings/realm` | Remove realm roles from group. |

## 4) Group management (routes 36-44, 9 routes)

| Method | Route | Why we use it |
|---|---|---|
| `GET` | `/admin/realms/{realm}/groups` | List groups. |
| `POST` | `/admin/realms/{realm}/groups` | Create group. |
| `GET` | `/admin/realms/{realm}/groups/{group_id}` | Get group details. |
| `PUT` | `/admin/realms/{realm}/groups/{group_id}` | Update group. |
| `DELETE` | `/admin/realms/{realm}/groups/{group_id}` | Delete group. |
| `GET` | `/admin/realms/{realm}/groups/{group_id}/members` | List group members. |
| `PUT` | `/admin/realms/{realm}/users/{user_id}/groups/{group_id}` | Add user to group. |
| `DELETE` | `/admin/realms/{realm}/users/{user_id}/groups/{group_id}` | Remove user from group. |
| `GET` | `/admin/realms/{realm}/group-by-path/{path}` | Resolve group by path. |

## 5) Client management (routes 45-51, 7 routes)

| Method | Route | Why we use it |
|---|---|---|
| `GET` | `/admin/realms/{realm}/clients` | List clients. |
| `POST` | `/admin/realms/{realm}/clients` | Create client. |
| `GET` | `/admin/realms/{realm}/clients/{client_id}` | Get client details. |
| `PUT` | `/admin/realms/{realm}/clients/{client_id}` | Update client config. |
| `DELETE` | `/admin/realms/{realm}/clients/{client_id}` | Delete client. |
| `GET` | `/admin/realms/{realm}/clients/{client_id}/client-secret` | Read client secret. |
| `POST` | `/admin/realms/{realm}/clients/{client_id}/client-secret` | Rotate client secret. |

## 6) Identity providers (routes 52-57, 6 routes)

| Method | Route | Why we use it |
|---|---|---|
| `GET` | `/admin/realms/{realm}/identity-provider/instances` | List IdP instances. |
| `POST` | `/admin/realms/{realm}/identity-provider/instances` | Create IdP instance (Google/social). |
| `GET` | `/admin/realms/{realm}/identity-provider/instances/{alias}` | Get IdP config. |
| `PUT` | `/admin/realms/{realm}/identity-provider/instances/{alias}` | Update IdP config. |
| `DELETE` | `/admin/realms/{realm}/identity-provider/instances/{alias}` | Delete IdP instance. |
| `POST` | `/admin/realms/{realm}/identity-provider/import-config` | Import provider config template/metadata. |

## 7) Realm config (routes 58-61, 4 routes)

| Method | Route | Why we use it |
|---|---|---|
| `GET` | `/admin/realms` | List realms for control-plane management. |
| `POST` | `/admin/realms` | Create realm (required for bootstrap). |
| `GET` | `/admin/realms/{realm}` | Get realm configuration. |
| `PUT` | `/admin/realms/{realm}` | Update realm configuration. |

## 8) Route count summary

- Authentication and token (`1-10`): `10`
- User CRUD and lifecycle (`11-24`): `14`
- Role management (`25-35`): `11`
- Group management (`36-44`): `9`
- Client management (`45-51`): `7`
- Identity providers (`52-57`): `6`
- Realm config (`58-61`): `4`

**Total selected routes: `61`**

## 9) Notes

- This list is intentionally constrained and excludes non-required alternates.
- It is aligned to your target of below 60 (safe margin under 65).
- Session inheritance safety baseline: `users/*/sessions` and `logout` routes support session control, but cross-realm handoff depends on successful child-realm `/auth` execution (typically `prompt=none`) plus explicit child entitlement checks.
