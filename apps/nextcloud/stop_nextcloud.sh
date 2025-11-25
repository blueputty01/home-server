#!/bin/bash

docker compose down

# Stop containers containing "nextcloud" in their name
docker stop $(docker ps -a | grep nextcloud | awk '{print $1}')

# Remove containers containing "nextcloud" in their name
docker rm $(docker ps -a | grep nextcloud | awk '{print $1}')

docker network rm nextcloud-aio
