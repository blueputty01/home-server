#!/bin/bash
set -euo pipefail

mkdir -p /app/logs
touch /app/logs/cron.log /app/logs/audio_playback.log

CRON_FILE="/etc/crontabs/root"
echo "SHELL=/bin/bash" > "$CRON_FILE"
echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" >> "$CRON_FILE"

# Each non-comment non-empty line must be
#   MIN HOUR DOM MON DOW ACTION
# ACTION = start|stop|restart
if [[ -n "${NOISE_CRON:-}" ]]; then
  while IFS= read -r rawline; do
    line="${rawline%%[[:space:]]*}" # preserve line for debug
    # Trim leading/trailing whitespace
    trimmed="$(echo "$rawline" | sed -e 's/^\s*//' -e 's/\s*$//')"
    [[ -z "$trimmed" || "${trimmed:0:1}" == "#" ]] && continue
    # Split into fields
    # shellcheck disable=SC2206
    parts=($trimmed)
    if [[ ${#parts[@]} -lt 6 ]]; then
      echo "Skipping invalid schedule (needs 5 cron fields + action): $trimmed" >> /app/logs/cron.log
      continue
    fi
    action="${parts[-1]}"
    cron_expr="${parts[0]} ${parts[1]} ${parts[2]} ${parts[3]} ${parts[4]}"
    case "$action" in
      start|stop|restart)
        echo "$cron_expr /usr/local/bin/noise-manager $action >> /app/logs/cron.log 2>&1" >> "$CRON_FILE"
        ;;
      *)
        echo "Skipping unknown action '$action' in line: $trimmed" >> /app/logs/cron.log
        ;;
    esac
  done <<< "$NOISE_CRON"
fi

echo "=== Active Crontab ==="
cat "$CRON_FILE"

# Start cron in foreground and also tail logs so container stays healthy.
# Use background tail and wait on cron (PID 1) so signals propagate.
crond -l 2 -f &
CRON_PID=$!

touch /app/logs/cron.log
# Concurrent tail for visibility (optional; won't exit container if cron stops unexpectedly)
tail -F /app/logs/cron.log &
TAIL_PID=$!

# Wait for cron; if it exits, also stop tail
wait $CRON_PID || EXIT_CODE=$?
kill $TAIL_PID 2>/dev/null || true
exit ${EXIT_CODE:-0}
