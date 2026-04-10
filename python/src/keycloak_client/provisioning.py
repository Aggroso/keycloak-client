from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .errors import ErrorContext, KeycloakApiError, KeycloakValidationError

if TYPE_CHECKING:
    from .client import KeycloakClient


async def ensure_realm(
    client: KeycloakClient,
    realm_name: str,
    *,
    create_payload: dict[str, Any] | None = None,
) -> bool:
    """Create a realm if it does not exist.

    Returns:
        True if the realm was created, False if it already existed.

    Raises:
        KeycloakApiError: If Keycloak returns an error other than 404 on the existence check.
    """
    try:
        await client.realms.get_realm(realm_name)
        return False
    except KeycloakApiError as exc:
        if exc.context.status_code != 404:
            raise
    payload = dict(create_payload or {})
    payload.setdefault("realm", realm_name)
    await client.realms.create_(payload=payload)
    return True


async def _client_internal_id(client: KeycloakClient, realm: str, client_id: str) -> str | None:
    found = await client.clients.get_realm_clients(realm, query={"clientId": client_id})
    if not found or not isinstance(found, list):
        return None
    if not found:
        return None
    internal = found[0].get("id")
    return str(internal) if internal else None


async def ensure_client_by_client_id(
    client: KeycloakClient,
    realm: str,
    *,
    client_id: str,
    create_payload: dict[str, Any],
) -> dict[str, Any]:
    """Return the client representation, creating it if missing (matched by ``clientId``)."""
    existing_id = await _client_internal_id(client, realm, client_id)
    if existing_id is not None:
        row = await client.clients.get_realm_clients_client_id(realm, existing_id)
        return row if isinstance(row, dict) else {}

    payload = dict(create_payload)
    payload.setdefault("clientId", client_id)
    await client.clients.create_realm_clients(realm, payload=payload)
    new_id = await _client_internal_id(client, realm, client_id)
    if new_id is None:
        raise KeycloakValidationError(
            "Client was created but could not be resolved by clientId",
            context=ErrorContext(
                operation="provisioning.ensure_client_by_client_id",
                status_code=None,
                retryable=False,
            ),
            details={"realm": realm, "clientId": client_id},
        )
    row = await client.clients.get_realm_clients_client_id(realm, new_id)
    return row if isinstance(row, dict) else {}


async def ensure_realm_role(
    client: KeycloakClient,
    realm: str,
    role_name: str,
    *,
    create_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the realm role, creating it if missing (matched by ``role_name``)."""
    try:
        role = await client.roles.get_realm_roles_role_name(realm, role_name)
        return role if isinstance(role, dict) else {}
    except KeycloakApiError as exc:
        if exc.context.status_code != 404:
            raise
    payload = {"name": role_name, **(create_payload or {})}
    await client.roles.create_realm_roles(realm, payload=payload)
    role = await client.roles.get_realm_roles_role_name(realm, role_name)
    return role if isinstance(role, dict) else {}


async def ensure_user_by_username(
    client: KeycloakClient,
    realm: str,
    username: str,
    *,
    create_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the user, creating it if missing (exact username match)."""
    users = await client.users.get_realm_users(
        realm, query={"username": username.strip(), "exact": True}
    )
    if isinstance(users, list) and users:
        row = users[0]
        return row if isinstance(row, dict) else {}
    payload = {"username": username.strip(), **(create_payload or {})}
    await client.users.create_realm_users(realm, payload=payload)
    users = await client.users.get_realm_users(
        realm, query={"username": username.strip(), "exact": True}
    )
    if not isinstance(users, list) or not users:
        raise KeycloakValidationError(
            "User was created but could not be loaded by username",
            context=ErrorContext(
                operation="provisioning.ensure_user_by_username", status_code=None, retryable=False
            ),
            details={"realm": realm, "username": username},
        )
    row = users[0]
    return row if isinstance(row, dict) else {}


async def ensure_protocol_mapper(
    client: KeycloakClient,
    realm: str,
    *,
    client_id: str,
    mapper: dict[str, Any],
) -> bool:
    """Create a client protocol mapper if one with the same ``name`` is not present.

    Returns:
        True if a mapper was created.

    Raises:
        KeycloakValidationError: If the client cannot be resolved.
    """
    mapper_name = mapper.get("name")
    if not mapper_name:
        raise KeycloakValidationError(
            "mapper payload must include a non-empty 'name' for idempotent ensure",
            context=ErrorContext(
                operation="provisioning.ensure_protocol_mapper", status_code=None, retryable=False
            ),
            details={},
        )
    internal_id = await _client_internal_id(client, realm, client_id)
    if internal_id is None:
        raise KeycloakValidationError(
            "Unknown clientId in realm",
            context=ErrorContext(
                operation="provisioning.ensure_protocol_mapper", status_code=None, retryable=False
            ),
            details={"realm": realm, "clientId": client_id},
        )
    path = f"/admin/realms/{realm}/clients/{internal_id}/protocol-mappers/models"
    listed = await client.transport.request("GET", path, auth_required=True)
    existing = listed.json()
    if isinstance(existing, list) and any(m.get("name") == mapper_name for m in existing):
        return False
    await client.transport.request("POST", path, json=mapper, auth_required=True)
    return True
