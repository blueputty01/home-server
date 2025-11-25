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

LOG_FILE="./logs/immich_backup.log"

{
  echo "=== Immich Backup Started at $(date) ==="
  echo "Backing up database from: ${DB_LOCATION}"
  echo "Backing up uploads from: ${UPLOAD_LOCATION}"
} >> "$LOG_FILE" 2>&1

borg create --stats --compression lz4 \
  ${BACKUP_REPO}::immich$(date +%F-%R) \
  ${DB_LOCATION} \
  ${UPLOAD_LOCATION} >> "$LOG_FILE" 2>&1
  
{
  echo "=== Immich Backup Completed at $(date) ==="
} >> "$LOG_FILE" 2>&1

docker compose up -d