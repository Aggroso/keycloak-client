from __future__ import annotations

from ..models.service_models import BootstrapOrgAuthorizationRequest, WorkflowResult
from .workflow_common import failed_result, run_step, success_result


class AuthorizationService:
    def __init__(self, client, observability) -> None:
        self._client = client
        self._obs = observability

    async def bootstrap_org_authorization(
        self, req: BootstrapOrgAuthorizationRequest
    ) -> WorkflowResult:
        cid = self._obs.correlation_id()
        admin_group = f"/orgs/{req.org_slug}/admins"
        member_group = f"/orgs/{req.org_slug}/members"
        try:
            await run_step(
                self._obs,
                workflow="bootstrap_org_authorization",
                step="create_admin_role",
                correlation_id=cid,
                fn=lambda: self._client.roles.create_realm_roles(
                    req.realm, payload={"name": req.admin_role_name}
                ),
            )
            await run_step(
                self._obs,
                workflow="bootstrap_org_authorization",
                step="create_member_role",
                correlation_id=cid,
                fn=lambda: self._client.roles.create_realm_roles(
                    req.realm, payload={"name": req.member_role_name}
                ),
            )
            admin_group_obj = await run_step(
                self._obs,
                workflow="bootstrap_org_authorization",
                step="create_admin_group",
                correlation_id=cid,
                fn=lambda: self._client.groups.create_realm_groups(
                    req.realm, payload={"name": admin_group}
                ),
            )
            member_group_obj = await run_step(
                self._obs,
                workflow="bootstrap_org_authorization",
                step="create_member_group",
                correlation_id=cid,
                fn=lambda: self._client.groups.create_realm_groups(
                    req.realm, payload={"name": member_group}
                ),
            )
            admin_group_id = (admin_group_obj or {}).get("id", "admins")
            member_group_id = (member_group_obj or {}).get("id", "members")
            await run_step(
                self._obs,
                workflow="bootstrap_org_authorization",
                step="map_admin_role_to_group",
                correlation_id=cid,
                fn=lambda: self._client.roles.create_realm_groups_group_id_role_mappings_realm(
                    req.realm, admin_group_id, payload=[{"name": req.admin_role_name}]
                ),
            )
            await run_step(
                self._obs,
                workflow="bootstrap_org_authorization",
                step="map_member_role_to_group",
                correlation_id=cid,
                fn=lambda: self._client.roles.create_realm_groups_group_id_role_mappings_realm(
                    req.realm, member_group_id, payload=[{"name": req.member_role_name}]
                ),
            )
            await run_step(
                self._obs,
                workflow="bootstrap_org_authorization",
                step="verify_admin_mapping",
                correlation_id=cid,
                fn=lambda: self._client.roles.get_realm_groups_group_id_role_mappings_realm(
                    req.realm, admin_group_id
                ),
            )
            await run_step(
                self._obs,
                workflow="bootstrap_org_authorization",
                step="verify_member_mapping",
                correlation_id=cid,
                fn=lambda: self._client.roles.get_realm_groups_group_id_role_mappings_realm(
                    req.realm, member_group_id
                ),
            )
            return success_result(
                correlation_id=cid,
                data={"admin_group_id": admin_group_id, "member_group_id": member_group_id},
            )
        except Exception as exc:
            return failed_result(
                correlation_id=cid, code="org_authorization_bootstrap_failed", message=str(exc)
            )
