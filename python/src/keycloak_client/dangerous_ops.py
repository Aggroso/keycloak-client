"""Phase 6: guardrails for high-impact admin operations."""

from __future__ import annotations

from .config import KeycloakClientConfig
from .errors import ErrorContext, KeycloakValidationError


def require_dangerous_operations_allowed(config: KeycloakClientConfig, operation: str) -> None:
    """Raise if ``operation`` requires explicit opt-in and config disallows it.

    Used for destructive or realm-wide side effects (e.g. realm delete compensation,
    ``logout-all``). Raw route modules remain unrestricted; call this from facades
    or services that perform dangerous workflows.
    """
    if not config.allow_dangerous_operations:
        raise KeycloakValidationError(
            (
                f"Operation '{operation}' requires "
                "KeycloakClientConfig.allow_dangerous_operations=True"
            ),
            context=ErrorContext(operation=operation, retryable=False),
        )
