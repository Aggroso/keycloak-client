#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

SKIP_INSTALL=0
SKIP_INTEGRATION=0
SKIP_OPENAPI=0

usage() {
  cat <<'EOF'
Pre-release validation runner for keycloak-client.

Usage:
  scripts/pre_release_validation.sh [options]

Options:
  --skip-install        Skip `pip install -e "./python[dev]"`.
  --skip-integration    Skip integration tests.
  --skip-openapi        Skip OpenAPI drift check.
  -h, --help            Show this help.

Environment (required unless --skip-integration):
  KEYCLOAK_INTEGRATION=1
  KEYCLOAK_BASE_URL=<staging keycloak url>
  KEYCLOAK_CLIENT_ID=<client id>
  KEYCLOAK_CLIENT_SECRET=<optional, can be empty for admin-cli>

Optional:
  KEYCLOAK_OPENAPI_URL=<override openapi url for drift check>
  PYTHON_BIN=<python executable, default: python3>
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-install) SKIP_INSTALL=1 ;;
    --skip-integration) SKIP_INTEGRATION=1 ;;
    --skip-openapi) SKIP_OPENAPI=1 ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 2
      ;;
  esac
  shift
done

run_step() {
  local title="$1"
  shift
  echo
  echo "==> ${title}"
  "$@"
}

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required environment variable: ${name}" >&2
    exit 2
  fi
}

cd "${ROOT_DIR}"

if [[ ${SKIP_INSTALL} -eq 0 ]]; then
  run_step "Python package install (dev extras)" bash -lc "
    ${PYTHON_BIN} -m pip install -e \"./python[dev]\" || \
    ${PYTHON_BIN} -m pip install \"./python[dev]\"
  "
else
  echo
  echo "==> Python package install skipped (--skip-install)"
fi

run_step "Ruff lint" bash -lc "cd python && ruff check src/keycloak_client"
run_step "Mypy type check" bash -lc "cd python && mypy src/keycloak_client"
run_step "Unit tests (no integration)" bash -lc \
  "cd python && pytest -q tests --ignore=tests/integration"

if [[ ${SKIP_INTEGRATION} -eq 0 ]]; then
  require_env "KEYCLOAK_INTEGRATION"
  require_env "KEYCLOAK_BASE_URL"
  require_env "KEYCLOAK_CLIENT_ID"
  if [[ "${KEYCLOAK_INTEGRATION}" != "1" ]]; then
    echo "KEYCLOAK_INTEGRATION must be set to 1 for real-env integration run." >&2
    exit 2
  fi
  run_step "Integration tests (real Keycloak env)" bash -lc \
    "cd python && pytest -q tests/integration -v"
else
  echo
  echo "==> Integration tests skipped (--skip-integration)"
fi

if [[ ${SKIP_OPENAPI} -eq 0 ]]; then
  run_step "OpenAPI drift check" bash -lc \
    "PYTHONPATH=python/src ${PYTHON_BIN} scripts/check_keycloak_openapi_drift.py"
else
  echo
  echo "==> OpenAPI drift check skipped (--skip-openapi)"
fi

echo
echo "Pre-release validation completed successfully."
