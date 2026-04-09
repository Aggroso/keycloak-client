from __future__ import annotations

from collections.abc import Mapping
from typing import Any

REDACTED = "[REDACTED]"
SENSITIVE_KEYS = {
    "authorization",
    "cookie",
    "set-cookie",
    "access_token",
    "refresh_token",
    "client_secret",
    "password",
    "secret",
}


def _is_sensitive(key: str) -> bool:
    key_l = key.lower()
    return key_l in SENSITIVE_KEYS or "token" in key_l or "secret" in key_l


def redact_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    return {k: redact_value(v) if not _is_sensitive(k) else REDACTED for k, v in value.items()}


def redact_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return redact_mapping(value)
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_value(item) for item in value)
    return value
