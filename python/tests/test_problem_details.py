from keycloak_client.models.service_models import WorkflowError
from keycloak_client.services.problem_details import to_problem_details


def test_problem_details_mapping() -> None:
    err = WorkflowError(code="x", message="boom", details={"a": 1})
    pd = to_problem_details(err, status=400, correlation_id="cid-1", instance="/test")
    assert pd["status"] == 400
    assert pd["detail"] == "boom"
    assert pd["extensions"]["code"] == "x"
    assert pd["extensions"]["correlation_id"] == "cid-1"
