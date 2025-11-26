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

echo "=== opencloud Backup Started at $(date) ==="

borg create --stats --compression lz4 \
  ${BACKUP_REPO}::opencloud$(date +%F-%R) \
  ${HDD_DATA_LOC}/opencloud \
  ${SSD_DATA_LOC}/opencloud
  
echo "=== opencloud Backup Completed at $(date) ==="

docker compose up -d