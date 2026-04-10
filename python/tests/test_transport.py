import asyncio

import httpx
import pytest

from keycloak_client.auth_provider import AuthProvider
from keycloak_client.config import KeycloakClientConfig
from keycloak_client.errors import KeycloakApiError, KeycloakTransportError
from keycloak_client.transport import Transport


def _cfg() -> KeycloakClientConfig:
    return KeycloakClientConfig(
        base_url="https://kc.example.com",
        realm="demo",
        client_id="admin-client",
        client_secret="secret",
    )


def test_transport_uses_injected_access_token_provider() -> None:
    async def run() -> None:
        paths: list[str] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            paths.append(request.url.path)
            assert request.headers.get("Authorization") == "Bearer injected"
            return httpx.Response(200, json={"ok": True})

        cfg = _cfg()
        auth = AuthProvider(cfg)

        async def provider(_client: httpx.AsyncClient) -> str:
            return "injected"

        tr = Transport(cfg, auth, access_token_provider=provider)
        tr._client = httpx.AsyncClient(
            base_url=cfg.base_url, transport=httpx.MockTransport(handler), verify=cfg.verify_tls
        )
        await tr.request("GET", "/admin/realms/demo/users")
        assert not any(p.endswith("/token") for p in paths)
        await tr.close()

    asyncio.run(run())


def test_transport_injects_auth_header() -> None:
    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path.endswith("/token"):
                return httpx.Response(200, json={"access_token": "abc", "expires_in": 60})
            assert request.headers["Authorization"] == "Bearer abc"
            return httpx.Response(200, json={"ok": True})

        transport = httpx.MockTransport(handler)
        cfg = _cfg()
        auth = AuthProvider(cfg)
        client = Transport(cfg, auth)
        client._client = httpx.AsyncClient(base_url=cfg.base_url, transport=transport, verify=cfg.verify_tls)
        response = await client.request("GET", "/admin/realms/demo/users")
        assert response.status_code == 200
        await client.close()

    asyncio.run(run())


def test_transport_raises_api_error_with_redaction() -> None:
    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path.endswith("/token"):
                return httpx.Response(200, json={"access_token": "abc", "expires_in": 60})
            return httpx.Response(401, json={"detail": "bad", "access_token": "secret-token"})

        transport = httpx.MockTransport(handler)
        cfg = _cfg()
        auth = AuthProvider(cfg)
        client = Transport(cfg, auth)
        client._client = httpx.AsyncClient(base_url=cfg.base_url, transport=transport, verify=cfg.verify_tls)
        with pytest.raises(KeycloakApiError) as exc:
            await client.request("GET", "/admin/realms/demo/users")
        assert exc.value.details["response"]["access_token"] == "[REDACTED]"
        await client.close()

    asyncio.run(run())


def test_transport_retries_connect_error_for_get_not_for_post() -> None:
    """Phase 6: only idempotent methods retry on transport-layer failures."""

    async def run() -> None:
        get_calls = {"n": 0}

        async def get_handler(request: httpx.Request) -> httpx.Response:
            if request.url.path.endswith("/token"):
                return httpx.Response(200, json={"access_token": "abc", "expires_in": 60})
            get_calls["n"] += 1
            if get_calls["n"] < 2:
                raise httpx.ConnectError("transient", request=request)
            return httpx.Response(200, json={"ok": True})

        cfg = _cfg()
        auth = AuthProvider(cfg)
        client = Transport(cfg, auth)
        client._client = httpx.AsyncClient(
            base_url=cfg.base_url, transport=httpx.MockTransport(get_handler), verify=cfg.verify_tls
        )
        response = await client.request("GET", "/admin/realms/demo/users")
        assert response.status_code == 200
        assert get_calls["n"] == 2
        await client.close()

        post_calls = {"n": 0}

        async def post_handler(request: httpx.Request) -> httpx.Response:
            if request.url.path.endswith("/token"):
                return httpx.Response(200, json={"access_token": "abc", "expires_in": 60})
            post_calls["n"] += 1
            raise httpx.ConnectError("fail", request=request)

        client2 = Transport(cfg, auth)
        client2._client = httpx.AsyncClient(
            base_url=cfg.base_url, transport=httpx.MockTransport(post_handler), verify=cfg.verify_tls
        )
        with pytest.raises(KeycloakTransportError):
            await client2.request("POST", "/admin/realms/demo/users", json={})
        assert post_calls["n"] == 1
        await client2.close()

    asyncio.run(run())


def test_transport_api_error_403_least_privilege_context() -> None:
    """Phase 6: forbidden responses surface status for least-privilege handling."""

    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path.endswith("/token"):
                return httpx.Response(200, json={"access_token": "abc", "expires_in": 60})
            return httpx.Response(403, json={"error": "HTTP 403 Forbidden"})

        cfg = _cfg()
        auth = AuthProvider(cfg)
        client = Transport(cfg, auth)
        client._client = httpx.AsyncClient(
            base_url=cfg.base_url, transport=httpx.MockTransport(handler), verify=cfg.verify_tls
        )
        with pytest.raises(KeycloakApiError) as exc:
            await client.request("GET", "/admin/realms/demo/users")
        assert exc.value.context.status_code == 403
        assert exc.value.context.retryable is False
        await client.close()

    asyncio.run(run())

