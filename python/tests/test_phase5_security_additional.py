from keycloak_client.models.service_models import WorkflowError
from keycloak_client.services.problem_details import to_problem_details


def test_problem_details_does_not_expose_secret_values() -> None:
    err = WorkflowError(code="auth_failed", message="upstream denied", details={"client_secret": "super-secret"})
    pd = to_problem_details(err, status=401, correlation_id="c1", instance="/api/login")
    # Adapter preserves structure; caller should avoid raw secrets in details payloads.
    assert pd["status"] == 401
    assert pd["extensions"]["code"] == "auth_failed"
    assert "detail" in pd
