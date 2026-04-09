from __future__ import annotations

import asyncio
from collections.abc import Mapping
from typing import Any

import httpx

from .auth_provider import AuthProvider
from .config import IDEMPOTENT_METHODS, KeycloakClientConfig
from .errors import ErrorContext, KeycloakApiError, KeycloakTransportError
from .redaction import redact_value


class Transport:
    def __init__(self, config: KeycloakClientConfig, auth_provider: AuthProvider) -> None:
        timeout = httpx.Timeout(
            connect=config.timeout.connect,
            read=config.timeout.read,
            write=config.timeout.write,
            pool=config.timeout.pool,
        )
        self._client = httpx.AsyncClient(
            base_url=config.base_url, timeout=timeout, verify=config.verify_tls
        )
        self._config = config
        self._auth_provider = auth_provider

    async def close(self) -> None:
        await self._client.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,
        data: Any | None = None,
        headers: Mapping[str, str] | None = None,
        auth_required: bool = True,
    ) -> httpx.Response:
        method_u = method.upper()
        attempts = self._config.retry.max_retries + 1
        last_exc: Exception | None = None
        merged_headers: dict[str, str] = dict(headers or {})

        if auth_required:
            token = await self._auth_provider.get_access_token(self._client)
            merged_headers["Authorization"] = f"Bearer {token}"

        for attempt in range(1, attempts + 1):
            try:
                response = await self._client.request(
                    method_u,
                    path,
                    params=params,
                    json=json,
                    data=data,
                    headers=merged_headers,
                )
            except httpx.HTTPError as exc:
                last_exc = exc
                if not self._should_retry(method_u, attempt):
                    raise KeycloakTransportError(
                        "Transport request failed",
                        context=ErrorContext(
                            operation=f"{method_u} {path}",
                            retryable=self._should_retry(method_u, attempt),
                        ),
                        details={"error": str(exc), "path": path},
                    ) from exc
                await asyncio.sleep(0.1 * attempt)
                continue

            if response.status_code >= 400:
                raise KeycloakApiError(
                    f"Keycloak API returned {response.status_code}",
                    context=ErrorContext(
                        operation=f"{method_u} {path}",
                        status_code=response.status_code,
                        retryable=self._is_retryable_status(response.status_code)
                        and self._should_retry(method_u, attempt),
                    ),
                    details=self._safe_error_details(path, method_u, response),
                )
            return response

        raise KeycloakTransportError(
            "Transport request failed after retries",
            context=ErrorContext(operation=f"{method_u} {path}", retryable=False),
            details={"path": path, "error": str(last_exc) if last_exc else "unknown"},
        )

    def _safe_error_details(
        self, path: str, method: str, response: httpx.Response
    ) -> dict[str, Any]:
        details: dict[str, Any] = {
            "path": path,
            "method": method,
            "status_code": response.status_code,
        }
        try:
            details["response"] = redact_value(response.json())
        except ValueError:
            details["response"] = response.text
        return details

    def _is_retryable_status(self, status_code: int) -> bool:
        return status_code in {408, 429, 500, 502, 503, 504}

    def _should_retry(self, method: str, attempt: int) -> bool:
        if attempt > self._config.retry.max_retries:
            return False
        return method in self._config.retry.retry_methods and method in IDEMPOTENT_METHODS
