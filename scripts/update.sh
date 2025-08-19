#!/usr/bin/env bash
# Rebuild the Docker image from scratch and remove dangling layers.
# Usage: ./scripts/update.sh
set -euo pipefail
# Rebuild the image and prune dangling layers
docker compose build --no-cache
docker image prune -f
echo "Update complete."
