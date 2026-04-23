#!/bin/bash

device="ELAN1200:00 04F3:309F Touchpad"

# Handle the mouse click first
if [[ "$BLOCK_BUTTON" -eq 1 ]] || [[ "$1" == "toggle" ]]; then
    state=$(xinput list-props "$device" | grep "Device Enabled" | grep -o "[01]$")
    if [ "$state" -eq 1 ]; then
        xinput disable "$device"
    else
        xinput enable "$device"
    fi
fi

# Read and display the current state
state=$(xinput list-props "$device" | grep "Device Enabled" | grep -o "[01]$")
if [ "$state" -eq 1 ]; then
    echo "TP ON"
else
    echo "TP OFF"
fi
