from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..transport import Transport


class GroupRoutes:
    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    async def get_realm_groups(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/groups"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_groups(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/groups"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_groups_group_id(
        self,
        realm,
        group_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/groups/{group_id}"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def update_realm_groups_group_id(
        self,
        realm,
        group_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/groups/{group_id}"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def delete_realm_groups_group_id(
        self,
        realm,
        group_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/groups/{group_id}"
        response = await self._transport.request(
            "DELETE", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()

    async def get_realm_groups_group_id_members(
        self,
        realm,
        group_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/groups/{group_id}/members"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def update_realm_users_user_id_groups_group_id(
        self,
        realm,
        user_id,
        group_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/groups/{group_id}"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def delete_realm_users_user_id_groups_group_id(
        self,
        realm,
        user_id,
        group_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/groups/{group_id}"
        response = await self._transport.request(
            "DELETE", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()

    async def get_realm_group_by_path_path(
        self,
        realm,
        path,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/group-by-path/{path}"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()


ROUTE_SPECS = [
    ("get_realm_groups", "GET", "/admin/realms/{realm}/groups", ["realm"], True),
    ("create_realm_groups", "POST", "/admin/realms/{realm}/groups", ["realm"], True),
    (
        "get_realm_groups_group_id",
        "GET",
        "/admin/realms/{realm}/groups/{group_id}",
        ["realm", "group_id"],
        True,
    ),
    (
        "update_realm_groups_group_id",
        "PUT",
        "/admin/realms/{realm}/groups/{group_id}",
        ["realm", "group_id"],
        True,
    ),
    (
        "delete_realm_groups_group_id",
        "DELETE",
        "/admin/realms/{realm}/groups/{group_id}",
        ["realm", "group_id"],
        True,
    ),
    (
        "get_realm_groups_group_id_members",
        "GET",
        "/admin/realms/{realm}/groups/{group_id}/members",
        ["realm", "group_id"],
        True,
    ),
    (
        "update_realm_users_user_id_groups_group_id",
        "PUT",
        "/admin/realms/{realm}/users/{user_id}/groups/{group_id}",
        ["realm", "user_id", "group_id"],
        True,
    ),
    (
        "delete_realm_users_user_id_groups_group_id",
        "DELETE",
        "/admin/realms/{realm}/users/{user_id}/groups/{group_id}",
        ["realm", "user_id", "group_id"],
        True,
    ),
    (
        "get_realm_group_by_path_path",
        "GET",
        "/admin/realms/{realm}/group-by-path/{path}",
        ["realm", "path"],
        True,
    ),
]
