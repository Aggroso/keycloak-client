from __future__ import annotations

from .authorization_service import AuthorizationService
from .bff_compatibility import BffCompatibilityService
from .client_service import ClientService
from .group_service import GroupService
from .inheritance_service import InheritanceService
from .observability import Observability
from .realm_service import RealmService
from .user_service import UserService


class ServiceRegistry:
    def __init__(self, client, observability: Observability | None = None) -> None:
        self.observability = observability or Observability()
        self.realm = RealmService(client, self.observability)
        self.client = ClientService(client, self.observability)
        self.user = UserService(client, self.observability)
        self.group = GroupService(client, self.observability)
        self.authorization = AuthorizationService(client, self.observability)
        self.inheritance = InheritanceService(client, self.observability)
        self.bff = BffCompatibilityService(client, self.observability)
