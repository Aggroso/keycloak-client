import asyncio
from types import SimpleNamespace

import pytest

from keycloak_client.errors import KeycloakValidationError
from keycloak_client.models.service_models import BootstrapRealmRequest
from keycloak_client.services.observability import Observability
from keycloak_client.services.realm_service import RealmService


class FakeRealms:
    async def create_(self, payload=None):
        return {"id": "r1"}

    async def update_realm(self, realm, payload=None):
        return {"realm": realm}

    async def get_realm(self, realm):
        return {"realm": realm}


class FakeRealmsUpdateFails(FakeRealms):
    async def update_realm(self, realm, payload=None):
        raise RuntimeError("config failed")


class FakeTransport:
    async def request(self, *args, **kwargs):
        return None


class FakeClient(SimpleNamespace):
    pass


def test_bootstrap_realm_success() -> None:
    async def run() -> None:
        client = FakeClient(
            realms=FakeRealms(),
            transport=FakeTransport(),
            config=SimpleNamespace(allow_dangerous_operations=False),
        )
        service = RealmService(client, Observability())
        result = await service.bootstrap_realm(BootstrapRealmRequest(realm="demo", realm_payload={"realm": "demo"}))
        assert result.status == "success"
        assert result.data["realm"] == "demo"

    asyncio.run(run())


def test_bootstrap_destructive_rollback_requires_dangerous_flag() -> None:
    async def run() -> None:
        client = FakeClient(
            realms=FakeRealmsUpdateFails(),
            transport=FakeTransport(),
            config=SimpleNamespace(allow_dangerous_operations=False),
        )
        service = RealmService(client, Observability())
        with pytest.raises(KeycloakValidationError):
            await service.bootstrap_realm(
                BootstrapRealmRequest(
                    realm="demo",
                    realm_payload={"realm": "demo"},
                    allow_destructive_rollback=True,
                )
            )

    asyncio.run(run())
