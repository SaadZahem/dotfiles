#!/bin/bash

# Get the current volume as a clean integer (e.g., 50)
volume=$(pamixer --get-volume)

# Check if muted (returns "true" or "false")
muted=$(pamixer --get-mute)

if [[ "$muted" == "true" ]]; then
    echo "MUTE (${volume}%)"
else
    echo "VOL ${volume}%"
fi
