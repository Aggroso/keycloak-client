import asyncio
from types import SimpleNamespace

from keycloak_client.models.service_models import OnboardUserRequest
from keycloak_client.services.observability import Observability
from keycloak_client.services.user_service import UserService


class FakeUsers:
    async def create_realm_users(self, realm, payload=None):
        return {"id": "u1"}

    async def update_realm_users_user_id_reset_password(self, realm, user_id, payload=None):
        return None

    async def update_realm_users_user_id_send_verify_email(self, realm, user_id):
        return None

    async def update_realm_users_user_id_execute_actions_email(self, realm, user_id, payload=None):
        return None

    async def delete_realm_users_user_id(self, realm, user_id):
        return None

    async def get_realm_users_user_id_sessions(self, realm, user_id):
        return [{"id": "s1"}]

    async def create_realm_users_user_id_logout(self, realm, user_id):
        return None


class FakeGroups:
    async def update_realm_users_user_id_groups_group_id(self, realm, user_id, group_id):
        return None


class FakeRoles:
    async def create_realm_users_user_id_role_mappings_realm(self, realm, user_id, payload=None):
        return None


class FakeClient(SimpleNamespace):
    pass


def test_onboard_user_success() -> None:
    async def run() -> None:
        client = FakeClient(users=FakeUsers(), groups=FakeGroups(), roles=FakeRoles())
        service = UserService(client, Observability())
        req = OnboardUserRequest(realm="demo", user_payload={"username": "a"}, group_ids=["g1"], send_verify_email=True)
        result = await service.onboard_user(req)
        assert result.status == "success"
        assert result.data["user_id"] == "u1"

    asyncio.run(run())


def test_terminate_user_access_success() -> None:
    async def run() -> None:
        client = FakeClient(users=FakeUsers(), groups=FakeGroups(), roles=FakeRoles())
        service = UserService(client, Observability())
        result = await service.terminate_user_access("demo", "u1")
        assert result.status == "success"
        assert result.data["terminated_sessions"][0]["id"] == "s1"

    asyncio.run(run())
