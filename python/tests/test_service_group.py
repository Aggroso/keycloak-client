import asyncio
from types import SimpleNamespace

from keycloak_client.services.group_service import GroupService
from keycloak_client.services.observability import Observability


class FakeGroups:
    async def create_realm_groups(self, realm, payload=None):
        return {"id": "g1"}


class FakeClient(SimpleNamespace):
    pass


def test_ensure_group_success() -> None:
    async def run() -> None:
        client = FakeClient(groups=FakeGroups())
        service = GroupService(client, Observability())
        result = await service.ensure_group("demo", {"name": "admins"})
        assert result.status == "success"
        assert result.data["group"]["id"] == "g1"

    asyncio.run(run())
