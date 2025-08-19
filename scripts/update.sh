#!/usr/bin/env bash
set -euo pipefail
# Rebuild the image and prune dangling layers
docker compose build --no-cache
docker image prune -f
echo "Update complete."