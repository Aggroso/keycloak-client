from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..transport import Transport


class IdentityProviderRoutes:
    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    async def get_realm_identity_provider_instances(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/identity-provider/instances"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_identity_provider_instances(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/identity-provider/instances"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_identity_provider_instances_alias(
        self,
        realm,
        alias,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/identity-provider/instances/{alias}"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def update_realm_identity_provider_instances_alias(
        self,
        realm,
        alias,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/identity-provider/instances/{alias}"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def delete_realm_identity_provider_instances_alias(
        self,
        realm,
        alias,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/identity-provider/instances/{alias}"
        response = await self._transport.request(
            "DELETE", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()

    async def create_realm_identity_provider_import_config(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/identity-provider/import-config"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()


ROUTE_SPECS = [
    (
        "get_realm_identity_provider_instances",
        "GET",
        "/admin/realms/{realm}/identity-provider/instances",
        ["realm"],
        True,
    ),
    (
        "create_realm_identity_provider_instances",
        "POST",
        "/admin/realms/{realm}/identity-provider/instances",
        ["realm"],
        True,
    ),
    (
        "get_realm_identity_provider_instances_alias",
        "GET",
        "/admin/realms/{realm}/identity-provider/instances/{alias}",
        ["realm", "alias"],
        True,
    ),
    (
        "update_realm_identity_provider_instances_alias",
        "PUT",
        "/admin/realms/{realm}/identity-provider/instances/{alias}",
        ["realm", "alias"],
        True,
    ),
    (
        "delete_realm_identity_provider_instances_alias",
        "DELETE",
        "/admin/realms/{realm}/identity-provider/instances/{alias}",
        ["realm", "alias"],
        True,
    ),
    (
        "create_realm_identity_provider_import_config",
        "POST",
        "/admin/realms/{realm}/identity-provider/import-config",
        ["realm"],
        True,
    ),
]
