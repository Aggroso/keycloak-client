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


async def post_token_and_parse_access_token(
    client: httpx.AsyncClient,
    path: str,
    data: dict[str, Any],
) -> AccessToken:
    """POST form data to a token endpoint and return a cached-style :class:`AccessToken`.

    Raises:
        KeycloakAuthError: On transport failure, HTTP error, or malformed JSON response.
    """
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


async def fetch_resource_owner_password_token(
    *,
    client: httpx.AsyncClient,
    admin_realm: str,
    client_id: str,
    username: str,
    password: str,
    client_secret: str = "",
) -> AccessToken:
    """Obtain an access token using the OAuth2 resource-owner-password (ROPC) grant.

    Uses the same error handling and redaction as :class:`AuthProvider`.

    Warning:
        ROPC is discouraged for interactive users (RFC 9700). Prefer authorization-code flows
        for people and client-credentials or injected tokens for server automation.

    Args:
        client: ``httpx.AsyncClient`` with ``base_url`` set to the Keycloak deployment root.
        admin_realm: Realm hosting the token endpoint (often ``master`` for admin-cli).
        client_id: OAuth client id (e.g. ``admin-cli``).
        username: Resource-owner username.
        password: Resource-owner password.
        client_secret: Optional client secret for confidential clients.
    """
    path = f"/realms/{admin_realm}/protocol/openid-connect/token"
    data: dict[str, Any] = {
        "grant_type": "password",
        "client_id": client_id,
        "username": username,
        "password": password,
    }
    if client_secret:
        data["client_secret"] = client_secret
    return await post_token_and_parse_access_token(client, path, data)


class AuthProvider:
    """Acquires and caches access tokens for Admin API calls.

    Default grant is **client credentials**. Optional **password** grant uses the same
    single-flight lock and expiry skew as client credentials.

    Phase 6 / security: concurrent callers share a single in-flight refresh via
    ``asyncio.Lock`` (double-checked pattern) so parallel requests do not stampede
    the token endpoint.
    """

    def __init__(self, config: KeycloakClientConfig) -> None:
        self._config = config
        self._token: AccessToken | None = None
        self._lock = asyncio.Lock()

    async def clear_token_cache(self) -> None:
        """Drop any cached token (e.g. after logout or credential rotation)."""
        async with self._lock:
            self._token = None

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
        if self._config.token_endpoint_grant == "password":
            data: dict[str, Any] = {
                "grant_type": "password",
                "client_id": self._config.client_id,
                "username": (self._config.resource_owner_username or "").strip(),
                "password": self._config.resource_owner_password or "",
            }
            if self._config.client_secret:
                data["client_secret"] = self._config.client_secret
            return await post_token_and_parse_access_token(client, path, data)

        data = {
            "grant_type": "client_credentials",
            "client_id": self._config.client_id,
            "client_secret": self._config.client_secret,
        }
        return await post_token_and_parse_access_token(client, path, data)
