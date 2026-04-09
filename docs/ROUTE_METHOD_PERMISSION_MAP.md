# Route Method and Permission Map (v1)

This document publishes the Python v1 route-to-method mapping and permission notes.

Canonical route scope remains:

- `docs/SELECTED_ROUTES_AND_USE_CASES.md` (61 selected routes)
- `python/src/keycloak_client/raw/*` `ROUTE_SPECS` (machine-readable source)

## Permission model summary

- `auth_required=True` on all admin routes in v1 raw modules.
- OIDC helper routes are exposed from `raw/auth.py`; admin token acquisition still uses server-side credentials.
- Dangerous operations are guarded at service/facade layer (`allow_dangerous_operations` gate), not by raw module exclusion.

## Python raw route families

| Family | Module | Route count | Typical permission scope |
|---|---|---:|---|
| Auth + token | `python/src/keycloak_client/raw/auth.py` | 10 | OIDC + admin realm/session ops |
| Users | `python/src/keycloak_client/raw/users.py` | 14 | manage-users |
| Roles | `python/src/keycloak_client/raw/roles.py` | 11 | manage-realm / view-realm / role-mapping |
| Groups | `python/src/keycloak_client/raw/groups.py` | 9 | manage-users / manage-groups |
| Clients | `python/src/keycloak_client/raw/clients.py` | 7 | manage-clients |
| Identity providers | `python/src/keycloak_client/raw/identity_providers.py` | 6 | manage-identity-providers |
| Realms | `python/src/keycloak_client/raw/realms.py` | 4 | create/manage realms (master-level admin) |

## Service-layer mappings (high-level workflows)

| Service workflow | Primary route families used | Permission notes |
|---|---|---|
| `services.realm.bootstrap_realm` | realms, clients | realm create/update; optional delete compensation is dangerous |
| `services.user.onboard_user` | users, groups, roles | user lifecycle + group/role mapping |
| `services.authorization.bootstrap_org_authorization` | roles, groups | role/group scaffolding and mappings |
| `services.bff.*` | auth, users | BFF auth workflows; use backend-only secrets |
| `services.inheritance.*` | auth, users, roles | child-realm entitlement checks required |

## Dangerous / high-impact operations

- `KeycloakClient.dangerous_realm_logout_all(realm)` requires
  `KeycloakClientConfig.allow_dangerous_operations=True`.
- Realm-delete compensation in `services.realm.bootstrap_realm` is gated by
  `allow_dangerous_operations`.

## Where to inspect exact mappings

- `python/src/keycloak_client/raw/auth.py` -> `ROUTE_SPECS`
- `python/src/keycloak_client/raw/users.py` -> `ROUTE_SPECS`
- `python/src/keycloak_client/raw/roles.py` -> `ROUTE_SPECS`
- `python/src/keycloak_client/raw/groups.py` -> `ROUTE_SPECS`
- `python/src/keycloak_client/raw/clients.py` -> `ROUTE_SPECS`
- `python/src/keycloak_client/raw/identity_providers.py` -> `ROUTE_SPECS`
- `python/src/keycloak_client/raw/realms.py` -> `ROUTE_SPECS`

