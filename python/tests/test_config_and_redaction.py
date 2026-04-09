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

