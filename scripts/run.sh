#!/usr/bin/env bash
set -euo pipefail
# Run the CLI in Docker without needing Poetry locally
docker compose run --rm app "$@"