#!/bin/bash

COMPOSE_ENV_FILES=.env
FILE="budget"

set -o allexport
source .env
set +o allexport

cd "$FILE"
echo "Starting $FILE"
echo $HDD_DATA_LOC
pwd
docker compose config

cd ..
