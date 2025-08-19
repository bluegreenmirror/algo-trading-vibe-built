#!/usr/bin/env bash
# Verify the development environment by rebuilding and running core checks.
# Usage: ./scripts/doctor.sh
set -euo pipefail

echo "== Rebuilding image =="
docker compose build

echo "== Python & path check inside container =="
docker compose run -T --rm --entrypoint python app -c 'import sys, pkgutil; print("python:", sys.version); print("site:", sys.path[:3]); print("click found:", pkgutil.find_loader("click") is not None)'

echo "== CLI hello =="
docker compose run -T --rm app hello

echo "== CLI help =="
docker compose run -T --rm app --help

echo "== Pytest =="
# call pytest directly to avoid module resolution ambiguity
docker compose run -T --rm --entrypoint pytest app -q
