#!/bin/bash

cd /home/user/docker

for FILE in *; do
    if [ -d "$FILE" ]; then
        cd "$FILE"

        docker compose up -d

        cd ..
    fi
done