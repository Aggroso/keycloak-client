import asyncio
from types import SimpleNamespace

from keycloak_client.models.service_models import BootstrapOrgAuthorizationRequest
from keycloak_client.services.authorization_service import AuthorizationService
from keycloak_client.services.observability import Observability


class FakeRoles:
    async def create_realm_roles(self, realm, payload=None):
        return {"name": payload["name"]}

    async def create_realm_groups_group_id_role_mappings_realm(self, realm, group_id, payload=None):
        return {"ok": True}

    async def get_realm_groups_group_id_role_mappings_realm(self, realm, group_id):
        return [{"name": "role"}]


class FakeGroups:
    async def create_realm_groups(self, realm, payload=None):
        return {"id": payload["name"]}


class FakeClient(SimpleNamespace):
    pass


def test_bootstrap_org_authorization_success() -> None:
    async def run() -> None:
        client = FakeClient(roles=FakeRoles(), groups=FakeGroups())
        service = AuthorizationService(client, Observability())
        req = BootstrapOrgAuthorizationRequest(realm="demo", org_slug="acme")
        result = await service.bootstrap_org_authorization(req)
        assert result.status == "success"
        assert "admin_group_id" in result.data

    asyncio.run(run())
