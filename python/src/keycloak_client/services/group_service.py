from __future__ import annotations

from ..models.service_models import WorkflowResult
from .workflow_common import failed_result, success_result


class GroupService:
    def __init__(self, client, observability) -> None:
        self._client = client
        self._obs = observability

    async def ensure_group(self, realm: str, group_payload: dict) -> WorkflowResult:
        cid = self._obs.correlation_id()
        try:
            created = await self._client.groups.create_realm_groups(realm, payload=group_payload)
            return success_result(correlation_id=cid, data={"group": created})
        except Exception as exc:
            return failed_result(correlation_id=cid, code="group_ensure_failed", message=str(exc))
