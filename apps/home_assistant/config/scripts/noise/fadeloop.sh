#!/bin/bash

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <audio_file>"
    echo "Example: $0 sound.wav"
    exit 1
fi

INPUT_FILE="$1"

# Check if file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found!"
    exit 1
fi

# Set up signal handling
cleanup() {
    echo -e "\nStopping playback..."
    kill $FFPLAY_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# First play with fade-in (5 seconds)
echo "Playing with fade-in..."
ffplay -i "$INPUT_FILE" -af "afade=t=in:st=0:d=5" -autoexit -nodisp 2>/dev/null &
FFPLAY_PID=$!
wait $FFPLAY_PID

# Subsequent loops without fade
echo "Looping without fade (Ctrl+C to exit)..."
while true; do
    ffplay -i "$INPUT_FILE" -autoexit -nodisp 2>/dev/null &
    FFPLAY_PID=$!
    wait $FFPLAY_PID
done
