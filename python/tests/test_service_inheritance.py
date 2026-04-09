import asyncio
from types import SimpleNamespace

from keycloak_client.models.service_models import ChildSessionInheritanceRequest, ParentLogoutPropagationRequest
from keycloak_client.services.inheritance_service import InheritanceService
from keycloak_client.services.observability import Observability


class FakeAuth:
    async def get_realm_oidc_openid_connect_auth(self, realm, query=None):
        return {"ok": True}

    async def create_realm_oidc_openid_connect_token(self, realm, payload=None):
        return {"access_token": "x"}

    async def create_realm_oidc_openid_connect_logout(self, realm, payload=None):
        return None


class FakeRoles:
    async def get_realm_users_user_id_role_mappings_realm(self, realm, user_id):
        return [{"name": "org_member"}]


class FakeUsers:
    async def create_realm_users_user_id_logout(self, realm, user_id):
        return None


class FakeClient(SimpleNamespace):
    pass


def test_inheritance_success() -> None:
    async def run() -> None:
        client = FakeClient(auth=FakeAuth(), roles=FakeRoles(), users=FakeUsers())
        svc = InheritanceService(client, Observability())
        req = ChildSessionInheritanceRequest(parent_realm="p", child_realm="c", subject_user_id="u1")
        result = await svc.attempt_child_session_inheritance(req)
        assert result.status == "success"
        assert result.data["outcome"] == "inherited"

    asyncio.run(run())


def test_logout_propagation_success() -> None:
    async def run() -> None:
        client = FakeClient(auth=FakeAuth(), roles=FakeRoles(), users=FakeUsers())
        svc = InheritanceService(client, Observability())
        req = ParentLogoutPropagationRequest(parent_realm="p", child_realm="c", subject_user_id="u1")
        result = await svc.propagate_parent_logout(req)
        assert result.status == "success"

    asyncio.run(run())
