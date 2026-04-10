import asyncio

import httpx
import pytest

from keycloak_client.auth_provider import AuthProvider
from keycloak_client.config import KeycloakClientConfig
from keycloak_client.errors import KeycloakAuthError


def _cfg() -> KeycloakClientConfig:
    return KeycloakClientConfig(
        base_url="https://kc.example.com",
        realm="demo",
        client_id="admin-client",
        client_secret="secret",
    )


def test_auth_provider_fetches_token() -> None:
    async def run() -> None:
        calls = {"count": 0}

        async def handler(request: httpx.Request) -> httpx.Response:
            calls["count"] += 1
            return httpx.Response(200, json={"access_token": "t1", "expires_in": 120})

        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(base_url="https://kc.example.com", transport=transport) as client:
            provider = AuthProvider(_cfg())
            token = await provider.get_access_token(client)
            assert token == "t1"
            again = await provider.get_access_token(client)
            assert again == "t1"
        assert calls["count"] == 1

    asyncio.run(run())


def test_auth_provider_raises_on_error() -> None:
    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"error": "invalid_client"})

        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(base_url="https://kc.example.com", transport=transport) as client:
            provider = AuthProvider(_cfg())
            with pytest.raises(KeycloakAuthError):
                await provider.get_access_token(client)

    asyncio.run(run())


def test_auth_provider_password_grant() -> None:
    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path.endswith("/token")
            body = request.content.decode()
            assert "grant_type=password" in body
            assert "username=admin" in body
            return httpx.Response(200, json={"access_token": "ropc", "expires_in": 120})

        transport = httpx.MockTransport(handler)
        cfg = KeycloakClientConfig(
            base_url="https://kc.example.com",
            realm="demo",
            client_id="admin-cli",
            client_secret="",
            token_endpoint_grant="password",
            resource_owner_username="admin",
            resource_owner_password="pw",
        )
        async with httpx.AsyncClient(base_url="https://kc.example.com", transport=transport) as client:
            provider = AuthProvider(cfg)
            token = await provider.get_access_token(client)
            assert token == "ropc"

    asyncio.run(run())


def test_auth_provider_single_flight() -> None:
    async def run() -> None:
        calls = {"count": 0}

        async def handler(request: httpx.Request) -> httpx.Response:
            calls["count"] += 1
            await asyncio.sleep(0.05)
            return httpx.Response(200, json={"access_token": "locked", "expires_in": 120})

        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(base_url="https://kc.example.com", transport=transport) as client:
            provider = AuthProvider(_cfg())
            results = await asyncio.gather(*[provider.get_access_token(client) for _ in range(10)])
            assert all(token == "locked" for token in results)
        assert calls["count"] == 1

    asyncio.run(run())

