import asyncio
from types import SimpleNamespace

from keycloak_client.models.bff_models import (
    BffError,
    BuildLoginUrlRequest,
    CompleteLoginRequest,
    LogoutRequest,
    RefreshSessionRequest,
    UserInfoRequest,
)
from keycloak_client.services.bff_compatibility import BffCompatibilityService
from keycloak_client.services.observability import Observability


class FakeAuth:
    async def create_realm_oidc_openid_connect_token(self, realm, payload=None):
        if payload.get("code") == "bad":
            raise RuntimeError("bad code")
        return {
            "access_token": "a",
            "refresh_token": "r",
            "expires_in": 300,
            "token_type": "Bearer",
            "scope": "openid",
        }

    async def create_realm_oidc_openid_connect_logout(self, realm, payload=None):
        return None

    async def get_realm_oidc_openid_connect_userinfo(self, realm, headers=None):
        if not headers or "Authorization" not in headers:
            raise RuntimeError("missing header")
        return {"sub": "u1", "email": "u@example.com"}


class FakeClient(SimpleNamespace):
    pass


def _client() -> FakeClient:
    cfg = SimpleNamespace(base_url="https://kc.example.com", client_id="svc", client_secret="topsecret")
    return FakeClient(auth=FakeAuth(), config=cfg)


def test_build_login_url_uses_public_base_when_set() -> None:
    async def run() -> None:
        cfg = SimpleNamespace(
            base_url="https://internal.kc",
            public_base_url="https://public.kc",
            client_id="svc",
            client_secret="topsecret",
        )
        svc = BffCompatibilityService(FakeClient(auth=FakeAuth(), config=cfg), Observability())
        res = await svc.build_login_url(
            BuildLoginUrlRequest(
                realm="demo",
                client_id="svc",
                redirect_uri="https://app/callback",
                state="s1",
                nonce="n1",
            )
        )
        assert res.login_url.startswith("https://public.kc/realms/demo/protocol/openid-connect/auth")

    asyncio.run(run())


def test_build_login_url() -> None:
    async def run() -> None:
        svc = BffCompatibilityService(_client(), Observability())
        res = await svc.build_login_url(
            BuildLoginUrlRequest(
                realm="demo",
                client_id="svc",
                redirect_uri="https://app/callback",
                state="s1",
                nonce="n1",
                code_challenge="abc",
            )
        )
        assert "protocol/openid-connect/auth" in res.login_url
        assert "state=s1" in res.login_url
        assert res.correlation_id

    asyncio.run(run())


def test_complete_login_success_and_invalid() -> None:
    async def run() -> None:
        svc = BffCompatibilityService(_client(), Observability())
        ok = await svc.complete_login(CompleteLoginRequest(realm="demo", authorization_code="good", redirect_uri="https://app/callback"))
        assert ok.access_token == "a"
        bad = await svc.complete_login(CompleteLoginRequest(realm="demo", authorization_code="", redirect_uri="https://app/callback"))
        assert bad.error is not None
        assert bad.error.code == "bff_invalid_request"

    asyncio.run(run())


def test_bff_observability_events_never_contain_token_material() -> None:
    """Phase 6: BFF workflow events must not leak tokens or client_secret."""

    async def run() -> None:
        events: list[dict] = []

        def hook(payload: dict) -> None:
            events.append(dict(payload))

        svc = BffCompatibilityService(_client(), Observability(event_hook=hook))
        await svc.complete_login(CompleteLoginRequest(realm="demo", authorization_code="good", redirect_uri="https://app/callback"))
        await svc.refresh_session(RefreshSessionRequest(realm="demo", refresh_token="rt"))
        for ev in events:
            for forbidden in ("access_token", "refresh_token", "client_secret", "id_token", "password"):
                if forbidden in ev:
                    assert ev[forbidden] == "[REDACTED]"
            blob = str(ev)
            assert "topsecret" not in blob

    asyncio.run(run())


def test_refresh_logout_userinfo_and_problem_details() -> None:
    async def run() -> None:
        svc = BffCompatibilityService(_client(), Observability())
        r = await svc.refresh_session(RefreshSessionRequest(realm="demo", refresh_token="rt"))
        assert r.refresh_token == "r"
        lo = await svc.logout(LogoutRequest(realm="demo", refresh_token="rt"))
        assert lo.success is True
        ui = await svc.user_info(UserInfoRequest(realm="demo", access_token="at"))
        assert ui.profile["sub"] == "u1"
        pd = svc.to_problem_details(error=ui.error or BffError(code="x", message="m"), status=400, correlation_id="cid")
        assert pd["status"] == 400

    asyncio.run(run())
