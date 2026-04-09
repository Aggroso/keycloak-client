# Integration Testing

## Local run
1. Start Keycloak:
   - `docker compose -f python/tests/integration/docker-compose.keycloak.yml up -d`
2. Export env vars:
   - `KEYCLOAK_INTEGRATION=1`
   - `KEYCLOAK_BASE_URL=http://localhost:8080`
   - `KEYCLOAK_CLIENT_ID=admin-cli`
   - `KEYCLOAK_CLIENT_SECRET=<if-required>`
3. Run tests:
   - `cd python && pytest -q tests/integration`

## CI (GitHub Actions)

Workflow: `.github/workflows/python-ci-release.yml`.

| Job | What runs |
|-----|-----------|
| **quality** | `ruff check`, `mypy`, unit tests (`pytest` with `tests/integration` ignored), wheel build |
| **openapi-drift** | `scripts/check_keycloak_openapi_drift.py` after `pip install -e "./python[dev]"` |
| **integration-keycloak** | Docker Keycloak image from workflow env `KEYCLOAK_IMAGE` (currently `quay.io/keycloak/keycloak:26.0.7`), health wait on `http://127.0.0.1:8080/realms/master`, then `pytest tests/integration` with `KEYCLOAK_INTEGRATION=1` |

Integration job environment (typical):

- `KEYCLOAK_INTEGRATION=1`
- `KEYCLOAK_BASE_URL=http://127.0.0.1:8080`
- `KEYCLOAK_CLIENT_ID=admin-cli`
- `KEYCLOAK_CLIENT_SECRET` empty for dev `admin-cli`

Tag releases still require **quality**, **openapi-drift**, and **integration-keycloak** to succeed before **publish-private** runs.
