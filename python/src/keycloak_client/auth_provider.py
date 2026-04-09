from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any

import httpx

from .config import KeycloakClientConfig
from .errors import ErrorContext, KeycloakAuthError
from .redaction import redact_value


@dataclass
class AccessToken:
    token: str
    expires_at: float

    def is_expired(self, *, skew_seconds: int) -> bool:
        return time.time() >= (self.expires_at - skew_seconds)


class AuthProvider:
    """Acquires and caches admin access tokens (client credentials).

    Phase 6 / security: concurrent callers share a single in-flight refresh via
    ``asyncio.Lock`` (double-checked pattern) so parallel requests do not stampede
    the token endpoint.
    """

    def __init__(self, config: KeycloakClientConfig) -> None:
        self._config = config
        self._token: AccessToken | None = None
        self._lock = asyncio.Lock()

    async def get_access_token(self, client: httpx.AsyncClient) -> str:
        if self._token and not self._token.is_expired(
            skew_seconds=self._config.token_refresh_skew_seconds
        ):
            return self._token.token

        async with self._lock:
            if self._token and not self._token.is_expired(
                skew_seconds=self._config.token_refresh_skew_seconds
            ):
                return self._token.token
            self._token = await self._fetch_token(client)
            return self._token.token

    async def _fetch_token(self, client: httpx.AsyncClient) -> AccessToken:
        path = f"/realms/{self._config.admin_realm}/protocol/openid-connect/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self._config.client_id,
            "client_secret": self._config.client_secret,
        }
        try:
            response = await client.post(path, data=data)
        except httpx.HTTPError as exc:
            raise KeycloakAuthError(
                "Failed to fetch access token",
                context=ErrorContext(operation="auth.fetch_token", retryable=True),
                details={"error": str(exc)},
            ) from exc

        if response.status_code >= 400:
            details: dict[str, Any] = {"status_code": response.status_code}
            try:
                details["response"] = redact_value(response.json())
            except ValueError:
                details["response"] = response.text
            raise KeycloakAuthError(
                "Token endpoint returned an error",
                context=ErrorContext(
                    operation="auth.fetch_token", status_code=response.status_code, retryable=False
                ),
                details=details,
            )

        payload = response.json()
        token = payload.get("access_token")
        expires_in = int(payload.get("expires_in", 60))
        if not token:
            raise KeycloakAuthError(
                "Token response missing access_token",
                context=ErrorContext(
                    operation="auth.fetch_token", status_code=response.status_code, retryable=False
                ),
                details=redact_value(payload),
            )
        return AccessToken(token=token, expires_at=time.time() + expires_in)
