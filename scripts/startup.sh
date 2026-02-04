#!/bin/bash

if [ ! -d "/mnt/extension" ]; then
  echo "Error: drive extension does not seem to be mounted" >&2
  exit 1
fi

skip=(home_assistant letterfeed server_stats)

set -o allexport
source .env
set +o allexport

START_DIR="$PWD"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
cd ../apps/

for FILE in *; do
  if [ -d "$FILE" ]; then
    for s in "${skip[@]}"; do
      [[ "$FILE" == "$s" ]] && continue 2
    done

    cd "$FILE"
    echo "Starting $FILE"
    docker compose up -d

    cd ..
  fi
done

cd "$START_DIR"

