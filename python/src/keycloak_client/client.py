from __future__ import annotations

from typing import Any

from .auth_provider import AuthProvider
from .config import KeycloakClientConfig
from .dangerous_ops import require_dangerous_operations_allowed
from .raw.auth import AuthRoutes
from .raw.clients import ClientRoutes
from .raw.groups import GroupRoutes
from .raw.identity_providers import IdentityProviderRoutes
from .raw.realms import RealmRoutes
from .raw.roles import RoleRoutes
from .raw.users import UserRoutes
from .services import ServiceRegistry
from .transport import Transport


class KeycloakClient:
    def __init__(self, config: KeycloakClientConfig) -> None:
        self.config = config
        self.auth_provider = AuthProvider(config)
        self.transport = Transport(config, self.auth_provider)

        self.auth = AuthRoutes(self.transport)
        self.users = UserRoutes(self.transport)
        self.roles = RoleRoutes(self.transport)
        self.groups = GroupRoutes(self.transport)
        self.clients = ClientRoutes(self.transport)
        self.identity_providers = IdentityProviderRoutes(self.transport)
        self.realms = RealmRoutes(self.transport)
        self.services = ServiceRegistry(self)

    async def dangerous_realm_logout_all(self, realm: str) -> Any:
        """POST ``/admin/realms/{realm}/logout-all`` (terminates all sessions).

        Requires ``allow_dangerous_operations``.
        """
        require_dangerous_operations_allowed(self.config, "admin.logout_all")
        return await self.auth.create_realm_logout_all(realm)

    async def aclose(self) -> None:
        await self.transport.close()
