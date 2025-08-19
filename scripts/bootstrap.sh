#!/usr/bin/env bash
# Install project dependencies and set up pre-commit hooks.
# Usage: ./scripts/bootstrap.sh
set -euo pipefail
poetry install
poetry run pre-commit install
echo "Bootstrap complete. Copy .env.example to .env (never commit .env)."

