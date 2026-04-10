from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from ..errors import KeycloakClientError
from ..models.bff_models import (
    BffError,
    BffTokenResult,
    BuildLoginUrlRequest,
    BuildLoginUrlResult,
    CompleteLoginRequest,
    LogoutRequest,
    LogoutResult,
    RefreshSessionRequest,
    UserInfoRequest,
    UserInfoResult,
)
from .problem_details import to_problem_details


class BffCompatibilityService:
    def __init__(self, client, observability) -> None:
        self._client = client
        self._obs = observability

    @staticmethod
    def _browser_base_url(config: Any) -> str:
        fn = getattr(config, "browser_base_url", None)
        if callable(fn):
            return str(fn()).rstrip("/")
        public = getattr(config, "public_base_url", None)
        base = str(getattr(config, "base_url", "")).rstrip("/")
        if public:
            return str(public).rstrip("/")
        return base

    def _map_token_payload(
        self, payload: dict[str, Any] | None, correlation_id: str
    ) -> BffTokenResult:
        payload = payload or {}
        return BffTokenResult(
            access_token=payload.get("access_token"),
            refresh_token=payload.get("refresh_token"),
            expires_in=payload.get("expires_in"),
            id_token=payload.get("id_token"),
            token_type=payload.get("token_type"),
            scope=payload.get("scope"),
            correlation_id=correlation_id,
        )

    def _to_bff_error(self, code: str, exc: Exception) -> BffError:
        if isinstance(exc, KeycloakClientError):
            return BffError(
                code=code, message=str(exc), details={"operation": exc.context.operation}
            )
        return BffError(code=code, message=str(exc))

    def to_problem_details(
        self, *, error: BffError, status: int, correlation_id: str, instance: str | None = None
    ) -> dict[str, Any]:
        from ..models.service_models import WorkflowError

        return to_problem_details(
            WorkflowError(code=error.code, message=error.message, details=error.details),
            status=status,
            correlation_id=correlation_id,
            instance=instance,
            title="BFF Compatibility Error",
        )

    async def build_login_url(self, req: BuildLoginUrlRequest) -> BuildLoginUrlResult:
        cid = self._obs.correlation_id()
        q = {
            "client_id": req.client_id,
            "redirect_uri": req.redirect_uri,
            "response_type": "code",
            "scope": req.scope,
            "state": req.state,
            "nonce": req.nonce,
        }
        if req.prompt:
            q["prompt"] = req.prompt
        if req.code_challenge:
            q["code_challenge"] = req.code_challenge
            q["code_challenge_method"] = req.code_challenge_method or "S256"
        base = self._browser_base_url(self._client.config)
        path = f"/realms/{req.realm}/protocol/openid-connect/auth"
        login_url = f"{base}{path}?{urlencode(q)}"
        self._obs.emit(
            "bff.build_login_url", {"realm": req.realm, "correlation_id": cid, "state": req.state}
        )
        return BuildLoginUrlResult(
            login_url=login_url, state=req.state, nonce=req.nonce, correlation_id=cid
        )

    async def complete_login(self, req: CompleteLoginRequest) -> BffTokenResult:
        cid = self._obs.correlation_id()
        if not req.authorization_code:
            return BffTokenResult(
                None,
                None,
                None,
                None,
                None,
                None,
                cid,
                error=BffError("bff_invalid_request", "authorization_code is required"),
            )
        payload = {
            "grant_type": "authorization_code",
            "code": req.authorization_code,
            "redirect_uri": req.redirect_uri,
            "client_id": req.client_id or self._client.config.client_id,
            "client_secret": self._client.config.client_secret,
        }
        if req.code_verifier:
            payload["code_verifier"] = req.code_verifier
        try:
            token = await self._client.auth.create_realm_oidc_openid_connect_token(
                req.realm, payload=payload
            )
            self._obs.emit("bff.complete_login", {"realm": req.realm, "correlation_id": cid})
            return self._map_token_payload(token, cid)
        except Exception as exc:
            return BffTokenResult(
                None,
                None,
                None,
                None,
                None,
                None,
                cid,
                error=self._to_bff_error("bff_auth_exchange_failed", exc),
            )

    async def refresh_session(self, req: RefreshSessionRequest) -> BffTokenResult:
        cid = self._obs.correlation_id()
        if not req.refresh_token:
            return BffTokenResult(
                None,
                None,
                None,
                None,
                None,
                None,
                cid,
                error=BffError("bff_invalid_request", "refresh_token is required"),
            )
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": req.refresh_token,
            "client_id": req.client_id or self._client.config.client_id,
            "client_secret": self._client.config.client_secret,
        }
        try:
            token = await self._client.auth.create_realm_oidc_openid_connect_token(
                req.realm, payload=payload
            )
            self._obs.emit("bff.refresh_session", {"realm": req.realm, "correlation_id": cid})
            return self._map_token_payload(token, cid)
        except Exception as exc:
            return BffTokenResult(
                None,
                None,
                None,
                None,
                None,
                None,
                cid,
                error=self._to_bff_error("bff_refresh_failed", exc),
            )

    async def logout(self, req: LogoutRequest) -> LogoutResult:
        cid = self._obs.correlation_id()
        payload = {}
        if req.refresh_token:
            payload["refresh_token"] = req.refresh_token
        if req.id_token_hint:
            payload["id_token_hint"] = req.id_token_hint
        if req.post_logout_redirect_uri:
            payload["post_logout_redirect_uri"] = req.post_logout_redirect_uri
        try:
            await self._client.auth.create_realm_oidc_openid_connect_logout(
                req.realm, payload=payload
            )
            self._obs.emit("bff.logout", {"realm": req.realm, "correlation_id": cid})
            return LogoutResult(success=True, correlation_id=cid)
        except Exception as exc:
            return LogoutResult(
                success=False,
                correlation_id=cid,
                error=self._to_bff_error("bff_logout_failed", exc),
            )

    async def user_info(self, req: UserInfoRequest) -> UserInfoResult:
        cid = self._obs.correlation_id()
        if not req.access_token:
            return UserInfoResult(
                profile=None,
                correlation_id=cid,
                error=BffError("bff_invalid_request", "access_token is required"),
            )
        try:
            profile = await self._client.auth.get_realm_oidc_openid_connect_userinfo(
                req.realm,
                headers={"Authorization": f"Bearer {req.access_token}"},
            )
            self._obs.emit("bff.user_info", {"realm": req.realm, "correlation_id": cid})
            return UserInfoResult(profile=profile or {}, correlation_id=cid)
        except Exception as exc:
            return UserInfoResult(
                profile=None,
                correlation_id=cid,
                error=self._to_bff_error("bff_userinfo_failed", exc),
            )
