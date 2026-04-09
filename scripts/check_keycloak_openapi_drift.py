#!/usr/bin/env python3
"""Verify v1 admin REST routes still exist in Keycloak Admin OpenAPI (structural drift check).

OIDC runtime paths (/realms/{realm}/protocol/...) are not part of the Admin OpenAPI document;
they are listed for visibility only and do not fail this check.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

# Admin route specs live on raw modules (machine-readable source of truth).
from keycloak_client.raw import auth as raw_auth
from keycloak_client.raw import clients as raw_clients
from keycloak_client.raw import groups as raw_groups
from keycloak_client.raw import identity_providers as raw_idp
from keycloak_client.raw import realms as raw_realms
from keycloak_client.raw import roles as raw_roles
from keycloak_client.raw import users as raw_users

DEFAULT_OPENAPI_URL = "https://www.keycloak.org/docs-api/latest/rest-api/openapi.json"


def _normalize_sdk_path_to_openapi(path: str) -> str:
    """Map SDK path templates to Keycloak OpenAPI path parameter style."""
    out = path.replace("/realms/master/", "/realms/{realm}/")
    out = out.replace("{user_id}", "{user-id}")
    # OpenAPI uses {groupId} on user-group join paths, {group-id} elsewhere.
    if "/users/{user-id}/groups/{group_id}" in out:
        out = out.replace("{group_id}", "{groupId}")
    else:
        out = out.replace("{group_id}", "{group-id}")
    out = out.replace("{client_id}", "{client-uuid}")
    out = out.replace("{role_name}", "{role-name}")
    return out


def _collect_specs() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for mod in (
        raw_auth,
        raw_realms,
        raw_users,
        raw_roles,
        raw_groups,
        raw_clients,
        raw_idp,
    ):
        for spec in mod.ROUTE_SPECS:
            _name, method, path, _params, _auth = spec
            rows.append((spec[0], method.upper(), path))
    return rows


def _load_openapi(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "keycloak-client-openapi-drift/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def _path_has_method(paths: dict[str, Any], path: str, method: str) -> bool:
    entry = paths.get(path)
    if not entry:
        return False
    return method.lower() in entry


def main() -> int:
    url = os.environ.get("KEYCLOAK_OPENAPI_URL", DEFAULT_OPENAPI_URL)
    try:
        doc = _load_openapi(url)
    except urllib.error.URLError as exc:
        print(f"ERROR: failed to fetch OpenAPI from {url}: {exc}", file=sys.stderr)
        return 2

    paths: dict[str, Any] = doc.get("paths") or {}
    admin_missing: list[tuple[str, str, str]] = []
    oidc_skipped: list[tuple[str, str, str]] = []

    for name, method, sdk_path in _collect_specs():
        if not sdk_path.startswith("/admin/"):
            oidc_skipped.append((name, method, sdk_path))
            continue
        openapi_path = _normalize_sdk_path_to_openapi(sdk_path)
        if not _path_has_method(paths, openapi_path, method):
            admin_missing.append((name, method, sdk_path, openapi_path))

    print(f"OpenAPI source: {url}")
    print(f"OIDC / non-admin routes (not in Admin OpenAPI): {len(oidc_skipped)}")
    for name, method, p in oidc_skipped:
        print(f"  skip  {method:6} {p}  ({name})")

    if admin_missing:
        print("MISSING admin operations vs OpenAPI:", file=sys.stderr)
        for name, method, sdk_path, openapi_path in admin_missing:
            print(f"  {method:6} SDK={sdk_path}  normalized={openapi_path}  ({name})", file=sys.stderr)
        return 1

    admin_count = len(_collect_specs()) - len(oidc_skipped)
    print(f"OK: all {admin_count} admin routes present in OpenAPI.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
