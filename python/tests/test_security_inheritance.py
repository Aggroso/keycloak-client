"""Phase 6: inheritance edge cases and logout propagation warnings."""

import asyncio
from types import SimpleNamespace

from keycloak_client.models.service_models import ChildSessionInheritanceRequest, ParentLogoutPropagationRequest
from keycloak_client.services.inheritance_service import InheritanceService
from keycloak_client.services.observability import Observability


class _AuthOk:
    async def get_realm_oidc_openid_connect_auth(self, realm, query=None):
        return {}

    async def create_realm_oidc_openid_connect_token(self, realm, payload=None):
        return {"access_token": "x"}

    async def create_realm_oidc_openid_connect_logout(self, realm, payload=None):
        return None


class _RolesEmptyList:
    async def get_realm_users_user_id_role_mappings_realm(self, realm, user_id):
        return []


class _RolesNone:
    async def get_realm_users_user_id_role_mappings_realm(self, realm, user_id):
        return None  # type: ignore[return-value]


class _UsersLogoutFails:
    async def create_realm_users_user_id_logout(self, realm, user_id):
        raise RuntimeError("child logout failed")


class _UsersLogoutOk:
    async def create_realm_users_user_id_logout(self, realm, user_id):
        return None


def test_inheritance_denied_when_roles_empty_or_none() -> None:
    async def run() -> None:
        for roles_impl in (_RolesEmptyList(), _RolesNone()):
            client = SimpleNamespace(auth=_AuthOk(), roles=roles_impl, users=_UsersLogoutOk())
            svc = InheritanceService(client, Observability())
            res = await svc.attempt_child_session_inheritance(
                ChildSessionInheritanceRequest(parent_realm="p", child_realm="c", subject_user_id="u1")
            )
            assert res.status == "failed"
            assert res.errors[0].code == "inheritance_denied"

    asyncio.run(run())


def test_propagate_parent_logout_warns_when_child_logout_fails() -> None:
    async def run() -> None:
        client = SimpleNamespace(auth=_AuthOk(), roles=_RolesEmptyList(), users=_UsersLogoutFails())
        svc = InheritanceService(client, Observability())
        res = await svc.propagate_parent_logout(
            ParentLogoutPropagationRequest(parent_realm="p", child_realm="c", subject_user_id="u1")
        )
        assert res.status == "success"
        assert any("Child logout propagation failed" in w for w in res.warnings)

    asyncio.run(run())
