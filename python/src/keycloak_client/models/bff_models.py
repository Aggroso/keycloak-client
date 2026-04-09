from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BffError:
    code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class BuildLoginUrlRequest:
    realm: str
    client_id: str
    redirect_uri: str
    state: str
    nonce: str
    scope: str = "openid profile email"
    prompt: str | None = None
    code_challenge: str | None = None
    code_challenge_method: str | None = None


@dataclass
class BuildLoginUrlResult:
    login_url: str
    state: str
    nonce: str
    correlation_id: str


@dataclass
class CompleteLoginRequest:
    realm: str
    authorization_code: str
    redirect_uri: str
    code_verifier: str | None = None
    client_id: str | None = None


@dataclass
class RefreshSessionRequest:
    realm: str
    refresh_token: str
    client_id: str | None = None


@dataclass
class LogoutRequest:
    realm: str
    refresh_token: str | None = None
    id_token_hint: str | None = None
    post_logout_redirect_uri: str | None = None


@dataclass
class UserInfoRequest:
    realm: str
    access_token: str


@dataclass
class BffTokenResult:
    access_token: str | None
    refresh_token: str | None
    expires_in: int | None
    id_token: str | None
    token_type: str | None
    scope: str | None
    correlation_id: str
    error: BffError | None = None


@dataclass
class LogoutResult:
    success: bool
    correlation_id: str
    error: BffError | None = None


@dataclass
class UserInfoResult:
    profile: dict[str, Any] | None
    correlation_id: str
    error: BffError | None = None
