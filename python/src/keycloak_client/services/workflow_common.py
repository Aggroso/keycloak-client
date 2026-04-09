from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from ..models.service_models import WorkflowError, WorkflowResult
from .observability import Observability


def success_result(
    *, correlation_id: str, data: dict[str, Any] | None = None, warnings: list[str] | None = None
) -> WorkflowResult:
    return WorkflowResult(
        status="success",
        data=data or {},
        warnings=warnings or [],
        correlation_id=correlation_id,
    )


def failed_result(
    *,
    correlation_id: str,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
    warnings: list[str] | None = None,
) -> WorkflowResult:
    return WorkflowResult(
        status="failed",
        errors=[WorkflowError(code=code, message=message, details=details or {})],
        warnings=warnings or [],
        correlation_id=correlation_id,
    )


async def run_step(
    obs: Observability,
    *,
    workflow: str,
    step: str,
    correlation_id: str,
    fn: Callable[[], Awaitable[Any]],
) -> Any:
    started = obs.start_timer()
    obs.emit(
        "workflow.step.start",
        {"workflow": workflow, "step": step, "correlation_id": correlation_id},
    )
    try:
        result = await fn()
    except Exception as exc:
        obs.emit(
            "workflow.step.failure",
            {
                "workflow": workflow,
                "step": step,
                "correlation_id": correlation_id,
                "elapsed_ms": obs.elapsed_ms(started),
                "error": str(exc),
            },
        )
        raise
    obs.emit(
        "workflow.step.success",
        {
            "workflow": workflow,
            "step": step,
            "correlation_id": correlation_id,
            "elapsed_ms": obs.elapsed_ms(started),
        },
    )
    return result
