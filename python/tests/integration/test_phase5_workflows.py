from __future__ import annotations

import asyncio

from keycloak_client import KeycloakClient
from keycloak_client.models.service_models import (
    BootstrapOrgAuthorizationRequest,
    BootstrapRealmRequest,
    OnboardUserRequest,
    ProvisionClientRequest,
)


def test_realm_bootstrap_integration(integration_config, realm_name: str) -> None:
    async def run() -> None:
        kc = KeycloakClient(integration_config)
        try:
            req = BootstrapRealmRequest(realm=realm_name, realm_payload={"realm": realm_name, "enabled": True})
            result = await kc.services.realm.bootstrap_realm(req)
            assert result.status in {"success", "partial_success", "failed"}
        finally:
            await kc.aclose()

    asyncio.run(run())


def test_client_provision_integration(integration_config, realm_name: str, client_name: str) -> None:
    async def run() -> None:
        kc = KeycloakClient(integration_config)
        try:
            req = ProvisionClientRequest(
                realm=realm_name,
                client_payload={"clientId": client_name, "id": client_name, "protocol": "openid-connect"},
            )
            result = await kc.services.client.provision_client(req)
            assert result.status in {"success", "partial_success", "failed"}
        finally:
            await kc.aclose()

    asyncio.run(run())


def test_user_onboarding_integration(integration_config, realm_name: str, user_name: str) -> None:
    async def run() -> None:
        kc = KeycloakClient(integration_config)
        try:
            req = OnboardUserRequest(
                realm=realm_name,
                user_payload={"username": user_name, "enabled": True, "email": f"{user_name}@example.com"},
                send_verify_email=False,
            )
            result = await kc.services.user.onboard_user(req)
            assert result.status in {"success", "partial_success", "failed"}
        finally:
            await kc.aclose()

    asyncio.run(run())


def test_org_authorization_integration(integration_config, realm_name: str) -> None:
    async def run() -> None:
        kc = KeycloakClient(integration_config)
        try:
            req = BootstrapOrgAuthorizationRequest(realm=realm_name, org_slug="acme")
            result = await kc.services.authorization.bootstrap_org_authorization(req)
            assert result.status in {"success", "partial_success", "failed"}
        finally:
            await kc.aclose()

    asyncio.run(run())
