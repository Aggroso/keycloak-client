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

## Related docs

- `docs/ROUTE_METHOD_PERMISSION_MAP.md`
- `docs/SECURITY_MODEL.md`
- `docs/INTEGRATION_TESTING.md`
