#!/bin/bash
set -euox pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/.."

# Source environment variables from project root
if [ -f "$PROJECT_ROOT/.env" ]; then
    source "$PROJECT_ROOT/.env"
fi

# Build multi-arch image and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag "$IMAGE_REPO/simple-python-app:latest" \
  --file "$SCRIPT_DIR/Dockerfile" \
  --push \
  "$PROJECT_ROOT"
