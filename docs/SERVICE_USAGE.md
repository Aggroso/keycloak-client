# Service Usage

## Initialize client
```python
from keycloak_client import KeycloakClient, KeycloakClientConfig

cfg = KeycloakClientConfig(
    base_url="https://keycloak.example.com",
    realm="master",
    admin_realm="master",
    client_id="svc-client",
    client_secret="***",
)
client = KeycloakClient(cfg)
```

Optional (see root `README.md` and `docs/CONSUMER_INTEGRATION_REQUIREMENTS.md`):

- **`public_base_url`**: browser-facing Keycloak URL for `build_login_url` while `base_url` stays internal.
- **`KeycloakClient(..., access_token_provider=...)`**: inject Admin API Bearer tokens (e.g. password-grant or vault-held tokens).
- **`token_endpoint_grant="password"`** (+ username/password on config): ROPC for bootstrap only; prefer service accounts.

## Idempotent provisioning helpers

For scripts and bootstrapping without duplicating HTTP glue:

```python
from keycloak_client import ensure_realm, ensure_user_by_username, ensure_client_by_client_id

await ensure_realm(client, "acme", create_payload={"enabled": True})
await ensure_client_by_client_id(
    client, "acme", client_id="api", create_payload={"protocol": "openid-connect"}
)
await ensure_user_by_username(client, "acme", "alice", create_payload={"enabled": True})
```

Sync callers: `from keycloak_client.sync_support import run_async` (scripts only; not from a running event loop).

## Bootstrap realm
```python
from keycloak_client.models.service_models import BootstrapRealmRequest

result = await client.services.realm.bootstrap_realm(
    BootstrapRealmRequest(realm="acme", realm_payload={"realm": "acme", "enabled": True})
)
```

## Onboard user
```python
from keycloak_client.models.service_models import OnboardUserRequest

result = await client.services.user.onboard_user(
    OnboardUserRequest(realm="acme", user_payload={"username": "alice", "enabled": True})
)
```

## BFF compatibility
```python
from keycloak_client.models.bff_models import BuildLoginUrlRequest, CompleteLoginRequest

login = await client.services.bff.build_login_url(
    BuildLoginUrlRequest(
        realm="acme",
        client_id="web-client",
        redirect_uri="https://app.example.com/callback",
        state="state-123",
        nonce="nonce-123",
    )
)

tokens = await client.services.bff.complete_login(
    CompleteLoginRequest(
        realm="acme",
        authorization_code="code-from-callback",
        redirect_uri="https://app.example.com/callback",
    )
)
```

## Session inheritance caveats

- Parent authentication does not grant child realm authorization automatically.
- Child entitlement checks must pass before local session establishment.
- Treat inheritance failures as expected fail-closed outcomes and handle retries/user prompts upstream.
- Threat model and reference flow: `docs/SESSION_INHERITANCE.md`.

## Related docs

- `docs/CONSUMER_INTEGRATION_REQUIREMENTS.md`
- `docs/SESSION_INHERITANCE.md`
- `docs/ROUTE_METHOD_PERMISSION_MAP.md`
- `docs/SECURITY_MODEL.md`
- `docs/INTEGRATION_TESTING.md`
