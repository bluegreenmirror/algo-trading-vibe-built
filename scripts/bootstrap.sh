#!/usr/bin/env bash
set -euo pipefail
poetry install
poetry run pre-commit install
echo "Bootstrap complete. Copy .env.example to .env (never commit .env)."
