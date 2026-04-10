from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

IDEMPOTENT_METHODS: frozenset[str] = frozenset({"GET", "HEAD", "OPTIONS"})


class RetryPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_retries: int = Field(default=2, ge=0, le=10)
    retry_methods: set[str] = Field(default_factory=lambda: set(IDEMPOTENT_METHODS))

    @field_validator("retry_methods")
    @classmethod
    def normalize_methods(cls, value: Iterable[str]) -> set[str]:
        methods = {item.upper() for item in value}
        if not methods:
            raise ValueError("retry_methods cannot be empty")
        return methods


class TimeoutConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    connect: float = Field(default=5.0, gt=0)
    read: float = Field(default=30.0, gt=0)
    write: float = Field(default=30.0, gt=0)
    pool: float = Field(default=5.0, gt=0)


class KeycloakClientConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    base_url: str
    """Internal/service URL for Admin API, token, JWKS, and server-side OIDC calls."""

    public_base_url: str | None = None
    """Optional browser-facing Keycloak base URL (e.g. public ingress). Used for BFF login URL
    construction only; Admin and token traffic still use ``base_url``."""

    realm: str
    admin_realm: str = "master"
    client_id: str
    client_secret: str = ""
    verify_tls: bool = True
    allow_dangerous_operations: bool = Field(
        default=False,
        description=(
            "Opt-in for destructive or realm-wide admin side effects "
            "(see docs/SECURITY_MODEL.md)."
        ),
    )
    token_refresh_skew_seconds: int = Field(default=60, ge=0, le=600)
    timeout: TimeoutConfig = Field(default_factory=TimeoutConfig)
    retry: RetryPolicy = Field(default_factory=RetryPolicy)

    token_endpoint_grant: Literal["client_credentials", "password"] = "client_credentials"
    """Grant used by :class:`~keycloak_client.auth_provider.AuthProvider` for Admin API tokens.

    ``password`` is the OAuth2 resource-owner-password grant (often called ROPC). Prefer
    client-credentials or an injected Bearer provider for production admin automation.
    """

    resource_owner_username: str | None = None
    resource_owner_password: str | None = None

    @field_validator("base_url")
    @classmethod
    def normalize_base_url(cls, value: str) -> str:
        clean = value.strip().rstrip("/")
        if not clean.startswith("http://") and not clean.startswith("https://"):
            raise ValueError("base_url must start with http:// or https://")
        return clean

    @field_validator("public_base_url")
    @classmethod
    def normalize_public_base_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        clean = value.strip().rstrip("/")
        if not clean.startswith("http://") and not clean.startswith("https://"):
            raise ValueError("public_base_url must start with http:// or https://")
        return clean

    @field_validator("realm", "admin_realm", "client_id")
    @classmethod
    def non_empty(cls, value: str) -> str:
        clean = value.strip()
        if not clean:
            raise ValueError("value cannot be empty")
        return clean

    @model_validator(mode="after")
    def password_grant_requires_credentials(self) -> KeycloakClientConfig:
        if self.token_endpoint_grant != "password":
            return self
        username = (self.resource_owner_username or "").strip()
        if not username:
            raise ValueError(
                "resource_owner_username is required when token_endpoint_grant is password"
            )
        if self.resource_owner_password is None:
            raise ValueError(
                "resource_owner_password is required when token_endpoint_grant is password"
            )
        return self

    def browser_base_url(self) -> str:
        """Base URL for browser redirects (BFF auth endpoint); falls back to ``base_url``."""
        return self.public_base_url or self.base_url


@dataclass(frozen=True)
class OperationContext:
    method: str
    path: str
