from __future__ import annotations

from ..models.service_models import (
    ChildSessionInheritanceRequest,
    ParentLogoutPropagationRequest,
    WorkflowResult,
)
from .workflow_common import failed_result, success_result


class InheritanceService:
    def __init__(self, client, observability) -> None:
        self._client = client
        self._obs = observability

    async def attempt_child_session_inheritance(
        self, req: ChildSessionInheritanceRequest
    ) -> WorkflowResult:
        cid = self._obs.correlation_id()
        try:
            prompt = "none" if req.prompt_none else "login"
            await self._client.auth.get_realm_oidc_openid_connect_auth(
                req.child_realm, query={"prompt": prompt}
            )
            # entitlement check placeholder from available selected routes
            roles = await self._client.roles.get_realm_users_user_id_role_mappings_realm(
                req.child_realm, req.subject_user_id
            )
            if not roles:
                return failed_result(
                    correlation_id=cid,
                    code="inheritance_denied",
                    message="Missing child entitlement",
                )
            token = await self._client.auth.create_realm_oidc_openid_connect_token(
                req.child_realm, payload={"grant_type": "refresh_token"}
            )
            if token:
                return success_result(correlation_id=cid, data={"outcome": "inherited"})
            return success_result(
                correlation_id=cid,
                data={"outcome": "interactive_login_required"},
                warnings=["Silent handoff did not establish child token"],
            )
        except Exception as exc:
            return failed_result(correlation_id=cid, code="inheritance_failed", message=str(exc))

    async def propagate_parent_logout(self, req: ParentLogoutPropagationRequest) -> WorkflowResult:
        cid = self._obs.correlation_id()
        warnings = []
        try:
            await self._client.auth.create_realm_oidc_openid_connect_logout(
                req.parent_realm, payload={}
            )
            try:
                await self._client.users.create_realm_users_user_id_logout(
                    req.child_realm, req.subject_user_id
                )
            except Exception:
                warnings.append("Child logout propagation failed; enforce short child TTL fallback")
            return success_result(
                correlation_id=cid,
                data={"parent_realm": req.parent_realm, "child_realm": req.child_realm},
                warnings=warnings,
            )
        except Exception as exc:
            return failed_result(
                correlation_id=cid,
                code="logout_propagation_failed",
                message=str(exc),
                warnings=warnings,
            )
