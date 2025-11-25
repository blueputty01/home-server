#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUDIO_SCRIPT="$SCRIPT_DIR/fadeloop.sh"
AUDIO_FILE="$SCRIPT_DIR/noise/white.mp3"
PID_FILE="$SCRIPT_DIR/logs/audio_playback.pid"
LOG_FILE="$SCRIPT_DIR/logs/audio_playback.log"

# if pid and log files don't exist
mkdir -p "$SCRIPT_DIR/logs"

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to start playback
start_playback() {
    # Check if already running
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Audio playback is already running (PID: $PID)"
            log "Start attempted but already running (PID: $PID)"
            return 1
        else
            # Remove stale PID file
            rm -f "$PID_FILE"
        fi
    fi

    # Validate audio script exists
    if [ ! -f "$AUDIO_SCRIPT" ]; then
        echo "Error: Audio script not found at $AUDIO_SCRIPT"
        log "Error: Audio script not found at $AUDIO_SCRIPT"
        return 1
    fi

    # Validate audio file exists
    if [ ! -f "$AUDIO_FILE" ]; then
        echo "Error: Audio file not found at $AUDIO_FILE"
        log "Error: Audio file not found at $AUDIO_FILE"
        return 1
    fi

    # Start the audio script in background
    "$AUDIO_SCRIPT" "$AUDIO_FILE" &
    SCRIPT_PID=$!
    echo $SCRIPT_PID > "$PID_FILE"
    
    echo "Audio playback started (PID: $SCRIPT_PID)"
    log "Audio playback started (PID: $SCRIPT_PID, File: $AUDIO_FILE)"
    
    # Wait a moment and check if it's still running
    sleep 2
    if ! kill -0 "$SCRIPT_PID" 2>/dev/null; then
        echo "Warning: Audio playback may have exited immediately"
        log "Warning: Audio playback process ended quickly"
        rm -f "$PID_FILE"
        return 1
    fi
    
    return 0
}

# Function to stop playback
stop_playback() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Audio playback is not running"
        log "Stop attempted but no PID file found"
        return 1
    fi

    PID=$(cat "$PID_FILE")
    
    if kill -0 "$PID" 2>/dev/null; then
        # Send SIGTERM first (graceful shutdown)
        kill "$PID"
        
        # Wait for process to exit
        for i in {1..10}; do
            if ! kill -0 "$PID" 2>/dev/null; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if kill -0 "$PID" 2>/dev/null; then
            kill -9 "$PID"
            echo "Audio playback forcefully stopped (PID: $PID)"
            log "Audio playback forcefully stopped (PID: $PID)"
        else
            echo "Audio playback stopped (PID: $PID)"
            log "Audio playback stopped gracefully (PID: $PID)"
        fi
    else
        echo "Audio playback was not running (stale PID file)"
        log "Stop attempted but process not running (stale PID: $PID)"
    fi
    
    # Clean up PID file
    rm -f "$PID_FILE"
    return 0
}

# Function to check status
status_playback() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Audio playback is running (PID: $PID)"
            return 0
        else
            echo "Audio playback is not running (stale PID file)"
            rm -f "$PID_FILE"
            return 1
        fi
    else
        echo "Audio playback is not running"
        return 1
    fi
}

# Function to show usage
usage() {
    echo "Usage: $0 {start|stop|restart|status|log}"
    echo ""
    echo "Commands:"
    echo "  start   - Start audio playback"
    echo "  stop    - Stop audio playback"
    echo "  restart - Restart audio playback"
    echo "  status  - Check if audio is playing"
    echo "  log     - Show recent logs"
    echo ""
    echo "Configure the script by editing:"
    echo "  AUDIO_SCRIPT: $AUDIO_SCRIPT"
    echo "  AUDIO_FILE: $AUDIO_FILE"
}

# Function to show logs
show_log() {
    if [ -f "$LOG_FILE" ]; then
        echo "=== Recent Audio Playback Logs ==="
        tail -20 "$LOG_FILE"
    else
        echo "No log file found at $LOG_FILE"
    fi
}

# Main command handler
case "$1" in
    start)
        start_playback
        ;;
    stop)
        stop_playback
        ;;
    restart)
        stop_playback
        sleep 2
        start_playback
        ;;
    status)
        status_playback
        ;;
    log)
        show_log
        ;;
    *)
        usage
        exit 1
        ;;
esac

exit $?