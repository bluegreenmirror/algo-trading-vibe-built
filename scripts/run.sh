#!/usr/bin/env bash
set -euo pipefail
set -x
# Forward all CLI args to the container's entrypoint
docker compose run --rm app "$@"