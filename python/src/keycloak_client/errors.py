from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ErrorContext:
    operation: str
    status_code: int | None = None
    retryable: bool = False


class KeycloakClientError(Exception):
    def __init__(
        self, message: str, *, context: ErrorContext, details: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message)
        self.context = context
        self.details = details or {}


class KeycloakAuthError(KeycloakClientError):
    pass


class KeycloakTransportError(KeycloakClientError):
    pass


class KeycloakApiError(KeycloakClientError):
    pass


class KeycloakValidationError(KeycloakClientError):
    pass
