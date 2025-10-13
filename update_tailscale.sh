#!/bin/bash

set -o allexport
source .env
set +o allexport

docker compose -f tailscale.yaml pull
./shutdown.sh
./startup.sh
