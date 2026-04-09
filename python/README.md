# keycloak-client (Python package)

Python SDK for Keycloak Admin and selected OIDC routes.

## Install

### From Git tag (recommended)

```bash
pip install "git+https://github.com/Aggroso/keycloak-client.git@v0.1.0#subdirectory=python"
```

### From source (this repository)

```bash
pip install -e "./python[dev]"
```

## Authentication configuration

The SDK currently uses `client_credentials` for admin token acquisition.

```python
from keycloak_client import KeycloakClient, KeycloakClientConfig

config = KeycloakClientConfig(
    base_url="https://keycloak.example.com",
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

