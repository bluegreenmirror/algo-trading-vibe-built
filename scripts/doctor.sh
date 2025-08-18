#!/usr/bin/env bash
set -euo pipefail

echo "== Rebuilding image =="
docker compose build

echo "== Python & path check inside container =="
docker compose run --rm app python -c "import sys, pkgutil; print('python:', sys.version); print('site:', sys.path[:3]); print('click found:', pkgutil.find_loader('click') is not None)"

echo "== CLI hello =="
docker compose run --rm app hello

echo "== CLI help =="
docker compose run --rm app --help