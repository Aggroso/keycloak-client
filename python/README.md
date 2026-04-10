# keycloak-client (Python package)

Python SDK for Keycloak Admin and selected OIDC routes.

> Requires Python `>=3.11`.

## Install

### From Git tag (recommended)

```bash
python3.11 -m pip install "git+https://github.com/Aggroso/keycloak-client.git@v0.1.2#subdirectory=python"
```

### From source (this repository)

```bash
python3.11 -m pip install -e "./python[dev]"
```

If your default `python3` is older (for example `3.9.x`), always call `python3.11 -m pip ...`.

## Authentication configuration

Default admin tokens use **client credentials**. Alternatives:

- **`token_endpoint_grant="password"`** plus `resource_owner_username` / `resource_owner_password` (ROPC; discouraged for interactive users).
- **`KeycloakClient(config, access_token_provider=async_callable)`** to supply a Bearer token for `/admin/*` yourself.

Use **`public_base_url`** when browsers must hit a public Keycloak hostname while the server uses **`base_url`** internally (BFF `build_login_url` only).

```python
from keycloak_client import KeycloakClient, KeycloakClientConfig

config = KeycloakClientConfig(
    base_url="https://keycloak.example.com",
    public_base_url="https://auth.example.com",  # optional
    realm="master",
    admin_realm="master",
    client_id="bootstrap-client",
    client_secret="***",
    verify_tls=True,
)
client = KeycloakClient(config)
```

## Common tasks

```python
# create a realm
await client.realms.create_(payload={"realm": "acme", "enabled": True})

# create a client inside that realm
await client.clients.create_realm_clients(
    "acme",
    payload={"clientId": "acme-web", "enabled": True, "protocol": "openid-connect"},
)
```

## Service workflow examples

```python
from keycloak_client.models.service_models import BootstrapRealmRequest, OnboardUserRequest

await client.services.realm.bootstrap_realm(
    BootstrapRealmRequest(realm="acme", realm_payload={"realm": "acme", "enabled": True}),
)

await client.services.user.onboard_user(
    OnboardUserRequest(realm="acme", user_payload={"username": "alice", "enabled": True}),
)
```

## Session inheritance caveats

- Parent authentication does not bypass child realm authorization checks.
- Child realms can enforce stronger policy than parent realms.
- Fail-closed behavior is expected on trust/policy failures.

## Validation before release

From repository root:

```bash
scripts/pre_release_validation.sh
```

For real Keycloak integration:

```bash
KEYCLOAK_INTEGRATION=1 \
KEYCLOAK_BASE_URL=https://<keycloak-host> \
KEYCLOAK_CLIENT_ID=<bootstrap-client-id> \
KEYCLOAK_CLIENT_SECRET=<bootstrap-client-secret> \
scripts/pre_release_validation.sh
```

