from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..transport import Transport


class ClientRoutes:
    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    async def get_realm_clients(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/clients"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_clients(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/clients"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_clients_client_id(
        self,
        realm,
        client_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/clients/{client_id}"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def update_realm_clients_client_id(
        self,
        realm,
        client_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/clients/{client_id}"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def delete_realm_clients_client_id(
        self,
        realm,
        client_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/clients/{client_id}"
        response = await self._transport.request(
            "DELETE", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()

    async def get_realm_clients_client_id_client_secret(
        self,
        realm,
        client_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/clients/{client_id}/client-secret"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_clients_client_id_client_secret(
        self,
        realm,
        client_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/clients/{client_id}/client-secret"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()


ROUTE_SPECS = [
    ("get_realm_clients", "GET", "/admin/realms/{realm}/clients", ["realm"], True),
    ("create_realm_clients", "POST", "/admin/realms/{realm}/clients", ["realm"], True),
    (
        "get_realm_clients_client_id",
        "GET",
        "/admin/realms/{realm}/clients/{client_id}",
        ["realm", "client_id"],
        True,
    ),
    (
        "update_realm_clients_client_id",
        "PUT",
        "/admin/realms/{realm}/clients/{client_id}",
        ["realm", "client_id"],
        True,
    ),
    (
        "delete_realm_clients_client_id",
        "DELETE",
        "/admin/realms/{realm}/clients/{client_id}",
        ["realm", "client_id"],
        True,
    ),
    (
        "get_realm_clients_client_id_client_secret",
        "GET",
        "/admin/realms/{realm}/clients/{client_id}/client-secret",
        ["realm", "client_id"],
        True,
    ),
    (
        "create_realm_clients_client_id_client_secret",
        "POST",
        "/admin/realms/{realm}/clients/{client_id}/client-secret",
        ["realm", "client_id"],
        True,
    ),
]
