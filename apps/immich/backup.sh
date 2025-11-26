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

echo "=== Immich Backup Started at $(date) ==="
echo "Backing up database from: ${DB_LOCATION}"
echo "Backing up uploads from: ${UPLOAD_LOCATION}"

borg create --stats --compression lz4 \
  ${BACKUP_REPO}::immich$(date +%F-%R) \
  ${DB_LOCATION} \
  ${UPLOAD_LOCATION}
  
echo "=== Immich Backup Completed at $(date) ==="

docker compose up -d