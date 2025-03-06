#!/bin/bash

set -o allexport
source .env
set +o allexport

./shutdown.sh
docker compose pull
./startup.sh
