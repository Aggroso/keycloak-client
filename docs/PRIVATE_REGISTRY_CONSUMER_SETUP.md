# Consumer Setup (Option B: Git tag install)

Use this guide to consume the SDK without a package registry.

## Python install from Git tag

Public repository:

```bash
python3.11 -m pip install "git+https://github.com/Aggroso/keycloak-client.git@v0.1.2#subdirectory=python"
```

Private repository (SSH):

```bash
python3.11 -m pip install "git+ssh://git@github.com/Aggroso/keycloak-client.git@v0.1.2#subdirectory=python"
```

## Pinning strategy

- Prefer release tags (`vX.Y.Z`) for stable consumption.
- Use commit SHAs only for hotfix testing.
- Avoid branch-based installs in production.
- Ensure the interpreter is Python `3.11+` (`python3.11 --version`).

## requirements.txt example

```txt
keycloak-client @ git+https://github.com/Aggroso/keycloak-client.git@v0.1.2#subdirectory=python
```

## TypeScript (deferred)

TypeScript package publishing is deferred until a `typescript/` package is added to this repo.

## Internal rollout checklist

- Release tag created and pushed (`vX.Y.Z`).
- CI quality + integration + drift jobs green for the tag.
- Consumer projects update Git tag dependency.

