import asyncio
from types import SimpleNamespace

from keycloak_client.models.service_models import ProvisionClientRequest
from keycloak_client.services.client_service import ClientService
from keycloak_client.services.observability import Observability


class FakeClients:
    async def create_realm_clients(self, realm, payload=None):
        return {"ok": True}

    async def get_realm_clients_client_id(self, realm, client_id):
        return {"id": client_id}

    async def create_realm_clients_client_id_client_secret(self, realm, client_id):
        return {"value": "rotated"}


class FakeClient(SimpleNamespace):
    pass


def test_provision_client_success() -> None:
    async def run() -> None:
        client = FakeClient(clients=FakeClients())
        service = ClientService(client, Observability())
        req = ProvisionClientRequest(realm="demo", client_payload={"clientId": "web"}, rotate_secret=True)
        result = await service.provision_client(req)
        assert result.status == "success"
        assert result.data["client_id"] == "web"

    asyncio.run(run())
