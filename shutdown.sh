#!/bin/bash

for FILE in *; do
  if [ -d "$FILE" ]; then
    cd "$FILE"
    echo "stopping $FILE"
    docker compose down

    cd ..
  fi
done
