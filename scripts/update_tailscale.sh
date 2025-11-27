#!/bin/bash

set -o allexport
source .env
set +o allexport

START_DIR="$PWD"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

docker compose -f ../shared/tailscale.yaml pull
./shutdown.sh
./startup.sh

cd "$START_DIR"
