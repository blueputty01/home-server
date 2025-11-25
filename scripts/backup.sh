#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/logs/backup.log"

LOG() { printf "\n%s %s\n\n" "$( date )" "$*" >> "$LOG_FILE" 2>&1; }
trap 'echo $( date ) Backup interrupted >> "$LOG_FILE" 2>&1; exit 2' INT TERM

borg create --stats --compression lz4 \
  ${BACKUP_REPO}::config$(date +%F-%R) \
  "$SCRIPT_DIR/.env" \
  --exclude "*/logs/*" \
  --exclude "*/docker_volumes/*" \
  >> "$LOG_FILE" 2>&1

backup_exit=$?

# Run the backup script for each app
for APP_DIR in "$SCRIPT_DIR"/apps/*; do
    if [ -d "$APP_DIR" ]; then
        BACKUP_SCRIPT="$APP_DIR/backup.sh"
        if [ -f "$BACKUP_SCRIPT" ]; then
            bash "$BACKUP_SCRIPT" >> "$LOG_FILE" 2>&1
            script_exit=$?
            if [ $script_exit -ne 0 ]; then
                LOG "Backup script for $(basename "$APP_DIR") failed with exit code $script_exit"
                backup_exit=$(( backup_exit > script_exit ? backup_exit : script_exit ))
            fi
        fi
    fi
done

borg prune                          \
    --list                          \
    --glob-archives '{hostname}-*'  \
    --show-rc                       \
    --keep-daily    7               \
    --keep-weekly   4               \
    --keep-monthly  6              \
    ${BACKUP_REPO}                  \
    >> "$LOG_FILE" 2>&1

prune_exit=$?

borg compact

compact_exit=$?

# use highest exit code as global exit code
global_exit=$(( backup_exit > prune_exit ? backup_exit : prune_exit ))
global_exit=$(( compact_exit > global_exit ? compact_exit : global_exit ))

if [ ${global_exit} -eq 0 ]; then
    info "Backup, Prune, and Compact finished successfully"
elif [ ${global_exit} -eq 1 ]; then
    info "Backup, Prune, and/or Compact finished with warnings"
else
    info "Backup, Prune, and/or Compact finished with errors"
fi

exit ${global_exit}
