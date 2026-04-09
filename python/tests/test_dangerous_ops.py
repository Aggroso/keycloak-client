"""Phase 6: dangerous operation guardrails."""

import asyncio

import httpx
import pytest

from keycloak_client import KeycloakClient, KeycloakClientConfig
from keycloak_client.errors import KeycloakValidationError


def test_dangerous_logout_all_requires_flag() -> None:
    async def run() -> None:
        cfg = KeycloakClientConfig(
            base_url="https://kc.example.com",
            realm="demo",
            client_id="admin",
            client_secret="s",
            allow_dangerous_operations=False,
        )
        client = KeycloakClient(cfg)
        with pytest.raises(KeycloakValidationError):
            await client.dangerous_realm_logout_all("demo")
        await client.aclose()

    asyncio.run(run())


def test_dangerous_logout_all_allowed_when_flag_set() -> None:
    async def run() -> None:
        calls: list[str] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path.endswith("/token"):
                return httpx.Response(200, json={"access_token": "t", "expires_in": 60})
            calls.append(request.url.path)
            return httpx.Response(204)

        cfg = KeycloakClientConfig(
            base_url="https://kc.example.com",
            realm="demo",
            client_id="admin",
            client_secret="s",
            allow_dangerous_operations=True,
        )
        client = KeycloakClient(cfg)
        client.transport._client = httpx.AsyncClient(base_url=cfg.base_url, transport=httpx.MockTransport(handler), verify=cfg.verify_tls)
        await client.dangerous_realm_logout_all("demo")
        assert any("logout-all" in p for p in calls)
        await client.aclose()

    asyncio.run(run())
