#!/bin/bash

set -o allexport
source .env
set +o allexport

for FILE in *; do
  if [ -d "$FILE" ]; then
    cd "$FILE"
    echo "Starting $FILE"
    docker compose config

    cd ..
  fi
done
