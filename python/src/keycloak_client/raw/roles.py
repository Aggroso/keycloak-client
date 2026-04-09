from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..transport import Transport


class RoleRoutes:
    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    async def get_realm_roles(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/roles"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_roles(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/roles"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_roles_role_name(
        self,
        realm,
        role_name,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/roles/{role_name}"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def update_realm_roles_role_name(
        self,
        realm,
        role_name,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/roles/{role_name}"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def delete_realm_roles_role_name(
        self,
        realm,
        role_name,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/roles/{role_name}"
        response = await self._transport.request(
            "DELETE", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()

    async def get_realm_users_user_id_role_mappings_realm(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/role-mappings/realm"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_users_user_id_role_mappings_realm(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/role-mappings/realm"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def delete_realm_users_user_id_role_mappings_realm(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/role-mappings/realm"
        response = await self._transport.request(
            "DELETE", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()

    async def create_realm_groups_group_id_role_mappings_realm(
        self,
        realm,
        group_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/groups/{group_id}/role-mappings/realm"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_groups_group_id_role_mappings_realm(
        self,
        realm,
        group_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/groups/{group_id}/role-mappings/realm"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def delete_realm_groups_group_id_role_mappings_realm(
        self,
        realm,
        group_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/groups/{group_id}/role-mappings/realm"
        response = await self._transport.request(
            "DELETE", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()


ROUTE_SPECS = [
    ("get_realm_roles", "GET", "/admin/realms/{realm}/roles", ["realm"], True),
    ("create_realm_roles", "POST", "/admin/realms/{realm}/roles", ["realm"], True),
    (
        "get_realm_roles_role_name",
        "GET",
        "/admin/realms/{realm}/roles/{role_name}",
        ["realm", "role_name"],
        True,
    ),
    (
        "update_realm_roles_role_name",
        "PUT",
        "/admin/realms/{realm}/roles/{role_name}",
        ["realm", "role_name"],
        True,
    ),
    (
        "delete_realm_roles_role_name",
        "DELETE",
        "/admin/realms/{realm}/roles/{role_name}",
        ["realm", "role_name"],
        True,
    ),
    (
        "get_realm_users_user_id_role_mappings_realm",
        "GET",
        "/admin/realms/{realm}/users/{user_id}/role-mappings/realm",
        ["realm", "user_id"],
        True,
    ),
    (
        "create_realm_users_user_id_role_mappings_realm",
        "POST",
        "/admin/realms/{realm}/users/{user_id}/role-mappings/realm",
        ["realm", "user_id"],
        True,
    ),
    (
        "delete_realm_users_user_id_role_mappings_realm",
        "DELETE",
        "/admin/realms/{realm}/users/{user_id}/role-mappings/realm",
        ["realm", "user_id"],
        True,
    ),
    (
        "create_realm_groups_group_id_role_mappings_realm",
        "POST",
        "/admin/realms/{realm}/groups/{group_id}/role-mappings/realm",
        ["realm", "group_id"],
        True,
    ),
    (
        "get_realm_groups_group_id_role_mappings_realm",
        "GET",
        "/admin/realms/{realm}/groups/{group_id}/role-mappings/realm",
        ["realm", "group_id"],
        True,
    ),
    (
        "delete_realm_groups_group_id_role_mappings_realm",
        "DELETE",
        "/admin/realms/{realm}/groups/{group_id}/role-mappings/realm",
        ["realm", "group_id"],
        True,
    ),
]
