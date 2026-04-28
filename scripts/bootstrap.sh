#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-${ROOT_DIR}/.venv}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "error: ${PYTHON_BIN} was not found. Install Python 3.12+ and retry." >&2
  exit 1
fi

"${PYTHON_BIN}" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)' || {
  echo "error: Python 3.12+ is required for meridian-core." >&2
  exit 1
}

cd "${ROOT_DIR}"

"${PYTHON_BIN}" -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/python" -m pip install --upgrade pip
"${VENV_DIR}/bin/python" -m pip install -e "tools/meridian-core[dev]"

cat <<'EOF'

Bootstrap complete.

Available local checks:
  make test
  make lint
  make typecheck
  make yaml
  make compose
  make check

Optional security checks, if Trivy is installed:
  make trivy-fs
  make trivy-config

Future MERIDIAN v2 detection bootstrap hooks are intentionally disabled until
the corresponding Falco rules, Kubernetes profiles, sample events, and Python
enrichment tooling exist.

Examples of future hooks, not active today:
  # kubectl apply -f deploy/profiles/local-k3s/
  # helm install falco falcosecurity/falco --namespace falco --create-namespace
  # python -m meridian_detect validate --events events/samples/
  # python -m meridian_detect report --output reports/local.json
EOF
