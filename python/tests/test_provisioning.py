import asyncio
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from keycloak_client.auth_provider import fetch_resource_owner_password_token
from keycloak_client.errors import ErrorContext, KeycloakApiError
from keycloak_client.provisioning import (
    ensure_client_by_client_id,
    ensure_protocol_mapper,
    ensure_realm,
    ensure_realm_role,
    ensure_user_by_username,
)


def test_fetch_resource_owner_password_token() -> None:
    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path.endswith("/token")
            body = request.content.decode()
            assert "grant_type=password" in body
            return httpx.Response(200, json={"access_token": "one-shot", "expires_in": 60})

        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(base_url="https://kc.example.com", transport=transport) as client:
            tok = await fetch_resource_owner_password_token(
                client=client,
                admin_realm="master",
                client_id="admin-cli",
                username="admin",
                password="pw",
            )
            assert tok.token == "one-shot"

    asyncio.run(run())


def test_ensure_realm_skips_when_present() -> None:
    async def run() -> None:
        client = MagicMock()
        client.realms.get_realm = AsyncMock(return_value={"realm": "acme"})
        client.realms.create_ = AsyncMock()
        assert await ensure_realm(client, "acme") is False
        client.realms.create_.assert_not_called()

    asyncio.run(run())


def test_ensure_realm_creates_on_404() -> None:
    async def run() -> None:
        client = MagicMock()
        missing = KeycloakApiError(
            "n",
            context=ErrorContext(operation="realms.get_realm", status_code=404),
        )
        client.realms.get_realm = AsyncMock(side_effect=missing)
        client.realms.create_ = AsyncMock(return_value=None)
        assert await ensure_realm(client, "acme", create_payload={"enabled": True}) is True
        client.realms.create_.assert_awaited_once_with(payload={"enabled": True, "realm": "acme"})

    asyncio.run(run())


def test_ensure_realm_propagates_non_404() -> None:
    async def run() -> None:
        client = MagicMock()
        err = KeycloakApiError(
            "x",
            context=ErrorContext(operation="realms.get_realm", status_code=403),
        )
        client.realms.get_realm = AsyncMock(side_effect=err)
        with pytest.raises(KeycloakApiError):
            await ensure_realm(client, "acme")

    asyncio.run(run())


def test_ensure_realm_role_creates_on_404() -> None:
    async def run() -> None:
        client = MagicMock()
        missing = KeycloakApiError(
            "n",
            context=ErrorContext(operation="roles.get", status_code=404),
        )
        call_n = 0

        async def get_role(*_a, **_k):
            nonlocal call_n
            call_n += 1
            if call_n == 1:
                raise missing
            return {"name": "viewer", "id": "1"}

        client.roles.get_realm_roles_role_name = AsyncMock(side_effect=get_role)
        client.roles.create_realm_roles = AsyncMock(return_value=None)
        out = await ensure_realm_role(client, "acme", "viewer", create_payload={"description": "x"})
        assert out["name"] == "viewer"
        client.roles.create_realm_roles.assert_awaited_once()

    asyncio.run(run())


def test_ensure_user_returns_existing() -> None:
    async def run() -> None:
        client = MagicMock()
        client.users.get_realm_users = AsyncMock(return_value=[{"id": "u1", "username": "alice"}])
        out = await ensure_user_by_username(client, "acme", "alice")
        assert out["id"] == "u1"
        client.users.create_realm_users.assert_not_called()

    asyncio.run(run())


def test_ensure_client_returns_existing() -> None:
    async def run() -> None:
        client = MagicMock()
        client.clients.get_realm_clients = AsyncMock(return_value=[{"id": "int-1", "clientId": "app"}])
        client.clients.get_realm_clients_client_id = AsyncMock(
            return_value={"id": "int-1", "clientId": "app"}
        )
        out = await ensure_client_by_client_id(
            client, "acme", client_id="app", create_payload={"protocol": "openid-connect"}
        )
        assert out["clientId"] == "app"
        client.clients.create_realm_clients.assert_not_called()

    asyncio.run(run())


def test_ensure_protocol_mapper_noop_when_name_exists() -> None:
    async def run() -> None:
        client = MagicMock()
        client.clients.get_realm_clients = AsyncMock(return_value=[{"id": "int-1", "clientId": "app"}])
        resp = MagicMock()
        resp.json.return_value = [{"name": "aud", "id": "m1"}]
        client.transport.request = AsyncMock(return_value=resp)
        created = await ensure_protocol_mapper(
            client,
            "acme",
            client_id="app",
            mapper={"name": "aud", "protocol": "openid-connect", "protocolMapper": "oidc-audience-mapper"},
        )
        assert created is False
        assert client.transport.request.await_count == 1

    asyncio.run(run())
