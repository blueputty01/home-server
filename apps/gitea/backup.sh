#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

set -o pipefail
set -u

set -o allexport
source ../.env
source ./.env
set +o allexport
docker compose down

borg create --stats --compression lz4 \
  ${BACKUP_REPO}::gitea$(date +%F-%R) \
  ${SSD_DATA_LOC}/gitea

docker compose up -d