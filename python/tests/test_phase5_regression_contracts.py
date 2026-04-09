from keycloak_client.services.problem_details import to_problem_details
from keycloak_client.models.service_models import WorkflowError


def test_problem_details_contract_fields() -> None:
    err = WorkflowError(code="route_failure", message="failed", details={"realm": "x"})
    pd = to_problem_details(err, status=502, correlation_id="cid", instance="/v1/op")
    assert set(["type", "title", "status", "detail", "extensions", "instance"]).issubset(set(pd.keys()))
    assert pd["extensions"]["code"] == "route_failure"
