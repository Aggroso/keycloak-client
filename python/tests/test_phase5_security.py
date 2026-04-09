import asyncio

from keycloak_client.models.service_models import ChildSessionInheritanceRequest
from keycloak_client.services.inheritance_service import InheritanceService
from keycloak_client.services.observability import Observability


class _FakeAuth:
    async def get_realm_oidc_openid_connect_auth(self, realm, query=None):
        return {"ok": True}

    async def create_realm_oidc_openid_connect_token(self, realm, payload=None):
        return None


class _FakeRolesNoEntitlement:
    async def get_realm_users_user_id_role_mappings_realm(self, realm, user_id):
        return []


class _FakeUsers:
    async def create_realm_users_user_id_logout(self, realm, user_id):
        return None


class _FakeClient:
    auth = _FakeAuth()
    roles = _FakeRolesNoEntitlement()
    users = _FakeUsers()


def test_fail_closed_when_entitlement_missing() -> None:
    async def run() -> None:
        svc = InheritanceService(_FakeClient(), Observability())
        result = await svc.attempt_child_session_inheritance(
            ChildSessionInheritanceRequest(parent_realm="p", child_realm="c", subject_user_id="u")
        )
        assert result.status == "failed"
        assert result.errors[0].code == "inheritance_denied"

    asyncio.run(run())
