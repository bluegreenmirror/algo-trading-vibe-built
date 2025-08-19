#!/usr/bin/env bash
# Run application commands inside the app container.
# Usage: ./scripts/run.sh <command> [args]
set -euo pipefail
set -x
# Forward all CLI args to the container's entrypoint
docker compose run --rm app "$@"
