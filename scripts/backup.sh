#!/usr/bin/env bash
set -u

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root." 
   exit 1
fi

# set working dir to root of project
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1
cd ../

set -o allexport
source .env
set +o allexport

./scripts/shutdown.sh

borg create --stats --compression lz4 \
  ${BACKUP_REPO}::all$(date +%F-%R) \
  ${HDD_DATA_LOC}                   \
  "$(pwd)"

backup_exit=$?

borg prune                          \
    ${BACKUP_REPO}                  \
    --list                          \
    --glob-archives '{hostname}-*'  \
    --show-rc                       \
    --keep-daily    7               \
    --keep-weekly   4               \
    --keep-monthly  6              \

prune_exit=$?

borg compact \
    ${BACKUP_REPO}

compact_exit=$?

./scripts/startup.sh

# use highest exit code as global exit code
global_exit=$(( backup_exit > prune_exit ? backup_exit : prune_exit ))
global_exit=$(( compact_exit > global_exit ? compact_exit : global_exit ))

if [ ${global_exit} -eq 0 ]; then
    echo "Backup, Prune, and Compact finished successfully"
elif [ ${global_exit} -eq 1 ]; then
    echo "Backup, Prune, and/or Compact finished with warnings"
else
    echo "Backup, Prune, and/or Compact finished with errors"
fi

exit ${global_exit}
