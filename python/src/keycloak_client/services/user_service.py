from __future__ import annotations

from typing import Any

from ..models.service_models import OnboardUserRequest, WorkflowResult
from .workflow_common import failed_result, run_step, success_result


class UserService:
    def __init__(self, client, observability) -> None:
        self._client = client
        self._obs = observability

    async def onboard_user(self, req: OnboardUserRequest) -> WorkflowResult:
        cid = self._obs.correlation_id()
        user_id = None
        try:
            created = await run_step(
                self._obs,
                workflow="onboard_user",
                step="create_user",
                correlation_id=cid,
                fn=lambda: self._client.users.create_realm_users(
                    req.realm, payload=req.user_payload
                ),
            )
            user_id = (
                (created or {}).get("id")
                or req.user_payload.get("id")
                or req.user_payload.get("username")
            )
            if req.temporary_password and user_id:
                await run_step(
                    self._obs,
                    workflow="onboard_user",
                    step="reset_password",
                    correlation_id=cid,
                    fn=lambda: self._client.users.update_realm_users_user_id_reset_password(
                        req.realm,
                        user_id,
                        payload={
                            "type": "password",
                            "value": req.temporary_password,
                            "temporary": True,
                        },
                    ),
                )
            for gid in req.group_ids:

                async def _add_user_group(captured_gid: str = gid) -> Any:
                    return await self._client.groups.update_realm_users_user_id_groups_group_id(
                        req.realm, user_id, captured_gid
                    )

                await run_step(
                    self._obs,
                    workflow="onboard_user",
                    step=f"add_group_{gid}",
                    correlation_id=cid,
                    fn=_add_user_group,
                )
            if req.realm_roles and user_id:
                await run_step(
                    self._obs,
                    workflow="onboard_user",
                    step="assign_roles",
                    correlation_id=cid,
                    fn=lambda: self._client.roles.create_realm_users_user_id_role_mappings_realm(
                        req.realm, user_id, payload=req.realm_roles
                    ),
                )
            if req.send_verify_email and user_id:
                await run_step(
                    self._obs,
                    workflow="onboard_user",
                    step="send_verify_email",
                    correlation_id=cid,
                    fn=lambda: self._client.users.update_realm_users_user_id_send_verify_email(
                        req.realm, user_id
                    ),
                )
            if req.execute_actions and user_id:
                await run_step(
                    self._obs,
                    workflow="onboard_user",
                    step="execute_actions",
                    correlation_id=cid,
                    fn=lambda: self._client.users.update_realm_users_user_id_execute_actions_email(
                        req.realm, user_id, payload=req.execute_actions
                    ),
                )
            return success_result(correlation_id=cid, data={"user_id": user_id})
        except Exception as exc:
            compensations = []
            if user_id and req.allow_destructive_rollback:
                try:
                    await self._client.users.delete_realm_users_user_id(req.realm, user_id)
                    compensations.append("delete_user")
                except Exception:
                    pass
            res = failed_result(correlation_id=cid, code="user_onboarding_failed", message=str(exc))
            res.compensations_applied = compensations
            return res

    async def terminate_user_access(self, realm: str, user_id: str) -> WorkflowResult:
        cid = self._obs.correlation_id()
        try:
            sessions = await self._client.users.get_realm_users_user_id_sessions(realm, user_id)
            await self._client.users.create_realm_users_user_id_logout(realm, user_id)
            return success_result(correlation_id=cid, data={"terminated_sessions": sessions or []})
        except Exception as exc:
            return failed_result(
                correlation_id=cid, code="terminate_user_access_failed", message=str(exc)
            )
