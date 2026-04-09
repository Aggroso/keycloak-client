from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..transport import Transport


class UserRoutes:
    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    async def get_realm_users(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_users(
        self,
        realm,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_users_user_id(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def update_realm_users_user_id(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def delete_realm_users_user_id(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}"
        response = await self._transport.request(
            "DELETE", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()

    async def update_realm_users_user_id_reset_password(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/reset-password"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def update_realm_users_user_id_send_verify_email(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/send-verify-email"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def update_realm_users_user_id_execute_actions_email(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/execute-actions-email"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_users_user_id_credentials(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/credentials"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def delete_realm_users_user_id_credentials_credentialId(
        self,
        realm,
        user_id,
        credentialId,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/credentials/{credentialId}"
        response = await self._transport.request(
            "DELETE", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if response.status_code == 204:
            return None
        if not response.content:
            return None
        return response.json()

    async def update_realm_users_user_id_disable_credential_types(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/disable-credential-types"
        response = await self._transport.request(
            "PUT", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_users_user_id_sessions(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/sessions"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def create_realm_users_user_id_logout(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/logout"
        response = await self._transport.request(
            "POST", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()

    async def get_realm_users_user_id_consents(
        self,
        realm,
        user_id,
        *,
        query: Mapping[str, Any] | None = None,
        payload: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        path = f"/admin/realms/{realm}/users/{user_id}/consents"
        response = await self._transport.request(
            "GET", path, params=query, json=payload, headers=headers, auth_required=True
        )
        if not response.content:
            return None
        return response.json()


ROUTE_SPECS = [
    ("get_realm_users", "GET", "/admin/realms/{realm}/users", ["realm"], True),
    ("create_realm_users", "POST", "/admin/realms/{realm}/users", ["realm"], True),
    (
        "get_realm_users_user_id",
        "GET",
        "/admin/realms/{realm}/users/{user_id}",
        ["realm", "user_id"],
        True,
    ),
    (
        "update_realm_users_user_id",
        "PUT",
        "/admin/realms/{realm}/users/{user_id}",
        ["realm", "user_id"],
        True,
    ),
    (
        "delete_realm_users_user_id",
        "DELETE",
        "/admin/realms/{realm}/users/{user_id}",
        ["realm", "user_id"],
        True,
    ),
    (
        "update_realm_users_user_id_reset_password",
        "PUT",
        "/admin/realms/{realm}/users/{user_id}/reset-password",
        ["realm", "user_id"],
        True,
    ),
    (
        "update_realm_users_user_id_send_verify_email",
        "PUT",
        "/admin/realms/{realm}/users/{user_id}/send-verify-email",
        ["realm", "user_id"],
        True,
    ),
    (
        "update_realm_users_user_id_execute_actions_email",
        "PUT",
        "/admin/realms/{realm}/users/{user_id}/execute-actions-email",
        ["realm", "user_id"],
        True,
    ),
    (
        "get_realm_users_user_id_credentials",
        "GET",
        "/admin/realms/{realm}/users/{user_id}/credentials",
        ["realm", "user_id"],
        True,
    ),
    (
        "delete_realm_users_user_id_credentials_credentialId",
        "DELETE",
        "/admin/realms/{realm}/users/{user_id}/credentials/{credentialId}",
        ["realm", "user_id", "credentialId"],
        True,
    ),
    (
        "update_realm_users_user_id_disable_credential_types",
        "PUT",
        "/admin/realms/{realm}/users/{user_id}/disable-credential-types",
        ["realm", "user_id"],
        True,
    ),
    (
        "get_realm_users_user_id_sessions",
        "GET",
        "/admin/realms/{realm}/users/{user_id}/sessions",
        ["realm", "user_id"],
        True,
    ),
    (
        "create_realm_users_user_id_logout",
        "POST",
        "/admin/realms/{realm}/users/{user_id}/logout",
        ["realm", "user_id"],
        True,
    ),
    (
        "get_realm_users_user_id_consents",
        "GET",
        "/admin/realms/{realm}/users/{user_id}/consents",
        ["realm", "user_id"],
        True,
    ),
]
