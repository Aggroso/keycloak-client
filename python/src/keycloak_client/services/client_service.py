from __future__ import annotations

from ..models.service_models import ProvisionClientRequest, WorkflowResult
from .workflow_common import failed_result, run_step, success_result


class ClientService:
    def __init__(self, client, observability) -> None:
        self._client = client
        self._obs = observability

    async def provision_client(self, req: ProvisionClientRequest) -> WorkflowResult:
        cid = self._obs.correlation_id()
        created_client_id = req.client_payload.get("id") or req.client_payload.get("clientId")
        try:
            await run_step(
                self._obs,
                workflow="provision_client",
                step="create_client",
                correlation_id=cid,
                fn=lambda: self._client.clients.create_realm_clients(
                    req.realm, payload=req.client_payload
                ),
            )
            client_data = None
            if created_client_id:
                client_data = await run_step(
                    self._obs,
                    workflow="provision_client",
                    step="read_client",
                    correlation_id=cid,
                    fn=lambda: self._client.clients.get_realm_clients_client_id(
                        req.realm, created_client_id
                    ),
                )
            secret_data = None
            if req.rotate_secret and created_client_id:
                secret_data = await run_step(
                    self._obs,
                    workflow="provision_client",
                    step="rotate_secret",
                    correlation_id=cid,
                    fn=lambda: self._client.clients.create_realm_clients_client_id_client_secret(
                        req.realm, created_client_id
                    ),
                )
            return success_result(
                correlation_id=cid,
                data={"client_id": created_client_id, "client": client_data, "secret": secret_data},
            )
        except Exception as exc:
            return failed_result(
                correlation_id=cid, code="client_provision_failed", message=str(exc)
            )
