from __future__ import annotations

from typing import Any

from ..models.service_models import WorkflowError


def to_problem_details(
    error: WorkflowError,
    *,
    status: int,
    correlation_id: str | None = None,
    instance: str | None = None,
    problem_type: str = "about:blank",
    title: str = "Workflow Error",
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "type": problem_type,
        "title": title,
        "status": status,
        "detail": error.message,
        "extensions": {
            "code": error.code,
            "details": error.details,
        },
    }
    if correlation_id:
        payload["extensions"]["correlation_id"] = correlation_id
    if instance:
        payload["instance"] = instance
    return payload
