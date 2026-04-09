"""Phase 6: expanded redaction coverage for headers-style keys and nesting."""

from keycloak_client.redaction import REDACTED, redact_value


def test_redact_nested_authorization_and_cookie_keys() -> None:
    payload = {
        "headers": {
            "Authorization": "Bearer secret-token",
            "Cookie": "session=abc",
            "Content-Type": "application/json",
        },
        "nested": {"Set-Cookie": "id=1"},
    }
    out = redact_value(payload)
    assert out["headers"]["Authorization"] == REDACTED
    assert out["headers"]["Cookie"] == REDACTED
    assert out["headers"]["Content-Type"] == "application/json"
    assert out["nested"]["Set-Cookie"] == REDACTED


def test_redact_list_of_mappings_with_secrets() -> None:
    rows = [{"access_token": "x"}, {"safe": "y"}]
    out = redact_value(rows)
    assert out[0]["access_token"] == REDACTED
    assert out[1]["safe"] == "y"


def test_redact_client_secret_key_case_insensitive_match() -> None:
    out = redact_value({"Client_Secret": "shh"})
    assert out["Client_Secret"] == REDACTED
