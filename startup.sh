#!/bin/bash

docker compose up -d

for FILE in *; do
  if [ -d "$FILE" ]; then
    cd "$FILE"
    echo "Starting $FILE"
    docker compose up -d

    cd ..
  fi
done
