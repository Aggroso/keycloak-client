# Private Registry Consumer Setup

Use this guide for installing/consuming SDK packages from internal registries.

## Python (pip)

### One-time install command

```bash
pip install --index-url https://<private-registry>/simple keycloak-client
```

### With `pip.conf` / `pip.ini`

Linux/macOS (`~/.config/pip/pip.conf`):

```ini
[global]
index-url = https://<username>:<token>@<private-registry>/simple
```

Windows (`%APPDATA%\pip\pip.ini`):

```ini
[global]
index-url = https://<username>:<token>@<private-registry>/simple
```

### Recommended authentication handling

- Use short-lived tokens from secrets manager or CI secret store.
- Avoid embedding credentials in committed files.
- Rotate private index credentials periodically.

## TypeScript (npm)

TypeScript package publishing is deferred until a `typescript/` package is added to this repo.

When available, consumer setup should use `.npmrc`:

```ini
@yourorg:registry=https://<private-npm-registry>/
//<private-npm-registry>/:_authToken=${NPM_TOKEN}
always-auth=true
```

## Internal rollout checklist

- Python package publish credentials configured in CI secrets.
- Consumer docs point to current private index URL.
- Security review confirms token storage/rotation policy.

