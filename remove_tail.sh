#!/bin/bash

set -o allexport
source .env
set +o allexport

for FILE in *; do
  if [ -d "$FILE" ]; then
    cd "$FILE"
    echo "removing tailscale dir from $FILE"
    sudo rm -rf tailscale
    cd ..
  fi
done
