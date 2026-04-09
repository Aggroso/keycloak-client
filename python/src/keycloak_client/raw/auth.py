from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..transport import Transport


class AuthRoutes:
    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    async def create_realm_oidc_openid_connect_token(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/realms/{realm}/protocol/openid-connect/token"
        response = await self._transport.request(
            "POST", path, params=query, data=payload, headers=headers, auth_required=False
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_oidc_openid_connect_logout(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/realms/{realm}/protocol/openid-connect/logout"
        response = await self._transport.request(
            "POST", path, params=query, data=payload, headers=headers, auth_required=False
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_oidc_openid_connect_userinfo(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/realms/{realm}/protocol/openid-connect/userinfo"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=False
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_oidc_openid_connect_certs(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/realms/{realm}/protocol/openid-connect/certs"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=False
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm__well_known_openid_configuration(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/realms/{realm}/.well-known/openid-configuration"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=False
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_oidc_openid_connect_auth(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/realms/{realm}/protocol/openid-connect/auth"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=False
        )
        if not response.content:
            return None
        return response.json()

    async def create_master_oidc_openid_connect_token(
        self,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = "/realms/master/protocol/openid-connect/token"
        response = await self._transport.request(
            "POST", path, params=query, data=payload, headers=headers, auth_required=False
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_logout_all(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/logout-all"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()

    async def get_realm_client_session_stats(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/client-session-stats"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_keys(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/keys"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()


ROUTE_SPECS = [
    (
        "create_realm_oidc_openid_connect_token",
        "POST",
        "/realms/{realm}/protocol/openid-connect/token",
        ["realm"],
        False,
    ),
    (
        "create_realm_oidc_openid_connect_logout",
        "POST",
        "/realms/{realm}/protocol/openid-connect/logout",
        ["realm"],
        False,
    ),
    (
        "get_realm_oidc_openid_connect_userinfo",
        "GET",
        "/realms/{realm}/protocol/openid-connect/userinfo",
        ["realm"],
        False,
    ),
    (
        "get_realm_oidc_openid_connect_certs",
        "GET",
        "/realms/{realm}/protocol/openid-connect/certs",
        ["realm"],
        False,
    ),
    (
        "get_realm__well_known_openid_configuration",
        "GET",
        "/realms/{realm}/.well-known/openid-configuration",
        ["realm"],
        False,
    ),
    (
        "get_realm_oidc_openid_connect_auth",
        "GET",
        "/realms/{realm}/protocol/openid-connect/auth",
        ["realm"],
        False,
    ),
    (
        "create_master_oidc_openid_connect_token",
        "POST",
        "/realms/master/protocol/openid-connect/token",
        [],
        False,
    ),
    ("create_realm_logout_all", "POST", "/admin/realms/{realm}/logout-all", ["realm"], True),
    (
        "get_realm_client_session_stats",
        "GET",
        "/admin/realms/{realm}/client-session-stats",
        ["realm"],
        True,
    ),
    ("get_realm_keys", "GET", "/admin/realms/{realm}/keys", ["realm"], True),
]
