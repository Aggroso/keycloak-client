from keycloak_client.services.observability import Observability


def test_observability_emits_redacted_event() -> None:
    events = []
    obs = Observability(event_hook=events.append)
    obs.emit("workflow.start", {"access_token": "secret", "realm": "demo"})
    assert events
    assert events[0]["access_token"] == "[REDACTED]"
    assert events[0]["realm"] == "demo"
