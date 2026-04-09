# keycloak-client

Production-oriented, Python-first Keycloak SDK for selected Admin and OIDC routes, with:

- Route-parity raw clients across 61 v1 operations
- Higher-level service workflows (realm/client/user/group/authorization)
- BFF compatibility helpers (`login`, `callback`, `refresh`, `logout`, `userinfo`)
- Security controls (redaction, fail-closed patterns, dangerous-op guardrails)

## Table of contents

- [Requirements](#requirements)
- [Architecture](#architecture)
- [Module boundaries](#module-boundaries)
- [Installation](#installation)
- [Bootstrap client setup (Keycloak)](#bootstrap-client-setup-keycloak)
- [Quick start](#quick-start)
- [Common usage](#common-usage)
- [Validation before release](#validation-before-release)
- [Documentation index](#documentation-index)

## Requirements

- Python `3.11+`
- Keycloak latest-stable target (see `docs/KEYCLOAK_COMPATIBILITY_POLICY.md`)
- Backend/server runtime for admin operations (`/admin/*` must not run in browsers)

## Architecture

The package uses a layered design:

- `config` -> typed runtime configuration
- `auth_provider` -> token acquisition/cache with single-flight refresh
- `transport` -> request execution, retries, auth header injection, error mapping
- `raw/*` -> endpoint-parity methods grouped by route family
- `services/*` -> orchestration workflows and BFF compatibility methods

## Module boundaries

- **Admin modules** (`raw/*`, `services/*`): backend only; never expose admin credentials to frontend code.
- **BFF compatibility** (`services/bff_compatibility.py`): browser-facing flow helpers with backend mediation.
- **Session inheritance** (`services/inheritance_service.py`): cross-realm trust handoff with mandatory child entitlement checks.

## Installation

Install from Git tag (recommended):

```bash
pip install "git+https://github.com/Aggroso/keycloak-client.git@v0.1.0#subdirectory=python"
```

Repository development install:

```bash
pip install -e "./python[dev]"
```

## Bootstrap client setup (Keycloak)

Use one dedicated automation client in `master` realm for provisioning (create realms/clients/users/roles/groups).

1. Sign in to Keycloak Admin Console and switch to `master`.
2. Create a client (example `client-bootstrap`).
3. Configure automation settings:
   - Client authentication: **Confidential**
   - Service accounts: **Enabled**
   - Browser/OIDC interactive flows: **Disabled** unless required for your use case
4. In **Credentials**, copy:
   - `client_id`
   - `client_secret`
5. In service-account role mappings, assign minimum required `realm-management` roles.

Export runtime variables:

```bash
export KEYCLOAK_BASE_URL="http://localhost:8080"
export KEYCLOAK_CLIENT_ID="client-bootstrap"
export KEYCLOAK_CLIENT_SECRET="<paste-secret>"
```

Security guidance:

- Store secrets in a vault/secret manager.
- Rotate secrets regularly.
- Keep bootstrap credentials for backend automation only.

## Quick start

```python
import asyncio

from keycloak_client import KeycloakClient, KeycloakClientConfig
from keycloak_client.models.service_models import BootstrapRealmRequest


async def main() -> None:
    cfg = KeycloakClientConfig(
        base_url="https://keycloak.example.com",
        realm="master",
        admin_realm="master",
        client_id="client-bootstrap",
        client_secret="***",
    )
    client = KeycloakClient(cfg)
    try:
        await client.services.realm.bootstrap_realm(
            BootstrapRealmRequest(
                realm="acme",
                realm_payload={"realm": "acme", "enabled": True},
            )
        )
    finally:
        await client.aclose()


asyncio.run(main())
```

## Common usage

```python
from keycloak_client.models.bff_models import BuildLoginUrlRequest
from keycloak_client.models.service_models import OnboardUserRequest

# Create a client in realm "acme"
await client.clients.create_realm_clients(
    "acme",
    payload={"clientId": "acme-api", "enabled": True, "protocol": "openid-connect"},
)

# Onboard user through service workflow
await client.services.user.onboard_user(
    OnboardUserRequest(realm="acme", user_payload={"username": "alice", "enabled": True}),
)

# Build BFF login URL
await client.services.bff.build_login_url(
    BuildLoginUrlRequest(
        realm="acme",
        client_id="web-client",
        redirect_uri="https://app.example.com/callback",
        state="state-123",
        nonce="nonce-123",
    )
)
```

Session inheritance behavior:

- Inheritance is trust handoff, not shared session object reuse.
- Child realm authorization is always required.
- Fail-closed behavior is expected on trust/policy failures.

## Validation before release

From repository root:

```bash
scripts/pre_release_validation.sh
```

Real-environment run:

```bash
KEYCLOAK_INTEGRATION=1 \
KEYCLOAK_BASE_URL=https://<keycloak-host> \
KEYCLOAK_CLIENT_ID=<bootstrap-client-id> \
KEYCLOAK_CLIENT_SECRET=<bootstrap-client-secret> \
scripts/pre_release_validation.sh
```

## Documentation index

- `python/README.md` - package-level setup and examples
- `docs/SERVICE_USAGE.md` - service workflows
- `docs/ROUTE_METHOD_PERMISSION_MAP.md` - route-to-method and permission guidance
- `docs/SECURITY_MODEL.md` - security controls and redaction policy
- `docs/INTEGRATION_TESTING.md` - local/CI integration testing
- `docs/OPENAPI_DRIFT.md` - OpenAPI drift checks
- `docs/PRIVATE_REGISTRY_CONSUMER_SETUP.md` - Git/pip consumer setup (Option B)
- `docs/RELEASE_PROCESS.md` and `docs/RELEASE_PIPELINES.md` - release execution and pipeline details
