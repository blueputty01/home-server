#!/bin/bash

if [ ! -d "/mnt/extension" ]; then
  echo "Error: drive extension does not seem to be mounted" >&2
  exit 1
fi

set -o allexport
source .env
set +o allexport

for FILE in *; do
  if [ -d "$FILE" ]; then
    cd "$FILE"
    echo "Starting $FILE"
    docker compose up -d

    cd ..
  fi
done
