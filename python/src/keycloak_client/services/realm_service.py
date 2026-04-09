from __future__ import annotations

from ..dangerous_ops import require_dangerous_operations_allowed
from ..errors import KeycloakValidationError
from ..models.service_models import BootstrapRealmRequest, WorkflowResult
from .workflow_common import failed_result, run_step, success_result


class RealmService:
    def __init__(self, client, observability) -> None:
        self._client = client
        self._obs = observability

    async def bootstrap_realm(self, req: BootstrapRealmRequest) -> WorkflowResult:
        cid = self._obs.correlation_id()
        self._obs.emit(
            "workflow.start",
            {"workflow": "bootstrap_realm", "correlation_id": cid, "realm": req.realm},
        )

        created = False
        try:
            await run_step(
                self._obs,
                workflow="bootstrap_realm",
                step="create_realm",
                correlation_id=cid,
                fn=lambda: self._client.realms.create_(payload=req.realm_payload),
            )
            created = True
            await run_step(
                self._obs,
                workflow="bootstrap_realm",
                step="update_realm",
                correlation_id=cid,
                fn=lambda: self._client.realms.update_realm(req.realm, payload=req.realm_payload),
            )
            await run_step(
                self._obs,
                workflow="bootstrap_realm",
                step="verify_realm",
                correlation_id=cid,
                fn=lambda: self._client.realms.get_realm(req.realm),
            )
            return success_result(correlation_id=cid, data={"realm": req.realm})
        except Exception as exc:
            compensations = []
            if created and req.allow_destructive_rollback:
                try:
                    require_dangerous_operations_allowed(
                        self._client.config,
                        "bootstrap_realm.compensation_delete_realm",
                    )
                    await self._client.transport.request(
                        "DELETE", f"/admin/realms/{req.realm}", auth_required=True
                    )
                    compensations.append("delete_realm")
                except KeycloakValidationError:
                    raise
                except Exception:
                    pass
            res = failed_result(correlation_id=cid, code="realm_bootstrap_failed", message=str(exc))
            res.compensations_applied = compensations
            return res
