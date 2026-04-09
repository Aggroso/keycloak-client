from __future__ import annotations

import os
import uuid

import pytest

from keycloak_client import KeycloakClientConfig


def _enabled() -> bool:
    return os.getenv("KEYCLOAK_INTEGRATION", "0") == "1"


def pytest_collection_modifyitems(items):
    if _enabled():
        return
    skip = pytest.mark.skip(reason="Set KEYCLOAK_INTEGRATION=1 to run integration tests")
    for item in items:
        if item.nodeid.startswith("tests/integration/"):
            item.add_marker(skip)


@pytest.fixture
def integration_config() -> KeycloakClientConfig:
    base_url = os.getenv("KEYCLOAK_BASE_URL", "http://localhost:8080")
    admin_realm = os.getenv("KEYCLOAK_ADMIN_REALM", "master")
    realm = os.getenv("KEYCLOAK_TEST_REALM", "master")
    client_id = os.getenv("KEYCLOAK_CLIENT_ID", "admin-cli")
    client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET", "")
    return KeycloakClientConfig(
        base_url=base_url,
        admin_realm=admin_realm,
        realm=realm,
        client_id=client_id,
        client_secret=client_secret,
        verify_tls=False,
    )


@pytest.fixture
def run_id() -> str:
    return uuid.uuid4().hex[:8]


@pytest.fixture
def realm_name(run_id: str) -> str:
    return f"phase5-{run_id}"


@pytest.fixture
def user_name(run_id: str) -> str:
    return f"phase5-user-{run_id}"


@pytest.fixture
def client_name(run_id: str) -> str:
    return f"phase5-client-{run_id}"


@pytest.fixture
def group_name(run_id: str) -> str:
    return f"phase5-group-{run_id}"
