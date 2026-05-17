#!/bin/bash

if [[ "$BLOCK_BUTTON" -eq 1 ]]; then
    dunstctl set-paused toggle
fi

if [[ "$(dunstctl is-paused)" == "false" ]]; then
    echo "NOTIF ON"
else
    echo "NOTIF OFF"
fi
