import pytest
from pydantic import ValidationError

from keycloak_client.config import KeycloakClientConfig
from keycloak_client.redaction import REDACTED, redact_value


def test_config_normalizes_base_url() -> None:
    cfg = KeycloakClientConfig(
        base_url="https://kc.example.com/",
        realm="demo",
        client_id="admin-cli",
        client_secret="secret",
    )
    assert cfg.base_url == "https://kc.example.com"


def test_config_public_base_url_normalized() -> None:
    cfg = KeycloakClientConfig(
        base_url="https://internal.example.com",
        public_base_url="https://public.example.com/",
        realm="demo",
        client_id="admin-cli",
        client_secret="secret",
    )
    assert cfg.public_base_url == "https://public.example.com"
    assert cfg.browser_base_url() == "https://public.example.com"


def test_config_password_grant_requires_credentials() -> None:
    with pytest.raises(ValidationError):
        KeycloakClientConfig(
            base_url="https://kc.example.com",
            realm="demo",
            client_id="admin-cli",
            client_secret="",
            token_endpoint_grant="password",
            resource_owner_username="",
            resource_owner_password="x",
        )
    with pytest.raises(ValidationError):
        KeycloakClientConfig(
            base_url="https://kc.example.com",
            realm="demo",
            client_id="admin-cli",
            client_secret="",
            token_endpoint_grant="password",
            resource_owner_username="admin",
            resource_owner_password=None,
        )


def test_redaction_masks_sensitive_keys() -> None:
    payload = {
        "access_token": "abc",
        "nested": {"client_secret": "hidden"},
        "safe": "value",
    }
    redacted = redact_value(payload)
    assert redacted["access_token"] == REDACTED
    assert redacted["nested"]["client_secret"] == REDACTED
    assert redacted["safe"] == "value"

