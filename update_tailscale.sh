#!/bin/bash

set -o allexport
source .env
set +o allexport

./shutdown.sh

docker compose -f tailscale.yaml pull
cd bare-git
docker compose build --no-cache --pull
cd ../
./startup.sh
