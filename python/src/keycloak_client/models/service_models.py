from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

WorkflowStatus = Literal["success", "partial_success", "failed"]


@dataclass
class WorkflowError:
    code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowResult:
    status: WorkflowStatus
    data: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[WorkflowError] = field(default_factory=list)
    compensations_applied: list[str] = field(default_factory=list)
    correlation_id: str | None = None


@dataclass
class BootstrapRealmRequest:
    realm: str
    realm_payload: dict[str, Any]
    allow_destructive_rollback: bool = False


@dataclass
class ProvisionClientRequest:
    realm: str
    client_payload: dict[str, Any]
    rotate_secret: bool = False
    allow_destructive_rollback: bool = False


@dataclass
class OnboardUserRequest:
    realm: str
    user_payload: dict[str, Any]
    group_ids: list[str] = field(default_factory=list)
    realm_roles: list[dict[str, Any]] = field(default_factory=list)
    send_verify_email: bool = False
    execute_actions: list[str] = field(default_factory=list)
    temporary_password: str | None = None
    allow_destructive_rollback: bool = False


@dataclass
class BootstrapOrgAuthorizationRequest:
    realm: str
    org_slug: str
    admin_role_name: str = "org_admin"
    member_role_name: str = "org_member"


@dataclass
class ChildSessionInheritanceRequest:
    parent_realm: str
    child_realm: str
    subject_user_id: str
    prompt_none: bool = True


@dataclass
class ParentLogoutPropagationRequest:
    parent_realm: str
    child_realm: str
    subject_user_id: str
