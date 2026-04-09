# Operations Runbook

## Observability
- Track `correlation_id` through workflow events.
- Validate payloads are redacted before emission.

## Common issues
- Token fetch failures: verify admin client permissions and secret.
- Realm bootstrap failures: check realm uniqueness and admin scopes.
- Inheritance denied: verify child entitlement role mappings.

## Remediation
- Re-run failed workflow with new correlation id after correcting permissions/config.
