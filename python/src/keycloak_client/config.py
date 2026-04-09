from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field, field_validator

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
    realm: str
    admin_realm: str = "master"
    client_id: str
    client_secret: str
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

    @field_validator("base_url")
    @classmethod
    def normalize_base_url(cls, value: str) -> str:
        clean = value.strip().rstrip("/")
        if not clean.startswith("http://") and not clean.startswith("https://"):
            raise ValueError("base_url must start with http:// or https://")
        return clean

    @field_validator("realm", "admin_realm", "client_id")
    @classmethod
    def non_empty(cls, value: str) -> str:
        clean = value.strip()
        if not clean:
            raise ValueError("value cannot be empty")
        return clean


@dataclass(frozen=True)
class OperationContext:
    method: str
    path: str
