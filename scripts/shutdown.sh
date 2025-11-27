#!/bin/bash

set -o allexport
source .env
set +o allexport

START_DIR="$PWD"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
cd ../apps/

for FILE in *; do
  if [ -d "$FILE" ]; then
    cd "$FILE"
    echo "stopping $FILE"
    docker compose down

    cd ..
  fi
done

cd "$START_DIR"