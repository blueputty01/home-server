#!/bin/bash

if [ ! -d "/mnt/extension" ]; then
  echo "Error: drive extension does not seem to be mounted" >&2
  exit 1
fi

set -o allexport
source .env
set +o allexport

START_DIR="$PWD"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
cd ../apps/

for FILE in *; do
  if [ -d "$FILE" ]; then
    if [ "${FILE}" == "home_assistant" ]; then
      continue
    fi
    cd "$FILE"
    echo "Starting $FILE"
    docker compose up -d

    cd ..
  fi
done

cd "$START_DIR"

