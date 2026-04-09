# Keycloak Compatibility Policy

## Supported target
- v1 supports latest-stable Keycloak.
- Compatibility is validated through CI integration runs.

For bumping the Keycloak version in CI and local harnesses, use [`KEYCLOAK_UPGRADE_WORKFLOW.md`](./KEYCLOAK_UPGRADE_WORKFLOW.md). Admin OpenAPI structural checks are described in [`OPENAPI_DRIFT.md`](./OPENAPI_DRIFT.md).

## Retest policy
- Required full retest on Keycloak major upgrade.
- Required integration + security retest on Keycloak minor upgrade.
- Required smoke retest on patch upgrades.

## Upgrade checklist
1. Bump integration image tag in integration harness.
2. Run unit + integration + security suites.
3. Validate service workflow outcomes remain contract-compatible.
4. Record results in release notes.
