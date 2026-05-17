#!/bin/bash

BAT="/sys/class/power_supply/BAT0"
CAPACITY=$(cat "$BAT/capacity")
STATUS=$(cat "$BAT/status")
CYCLE_COUNT=$(cat "$BAT/cycle_count")
STATE_FILE="$HOME/.local/state/battery_notified"

# Ensure the state directory exists
mkdir -p "${STATE_FILE%/*}"

# 1. Determine the icon based on charging status
ICON="🔋"
if [[ "$STATUS" == "Charging" ]]; then
    ICON="⚡"
elif [[ "$STATUS" == "Discharging" ]]; then
    ICON=""
elif [[ "$STATUS" == "Full" ]]; then
    ICON="🔌"
fi

# 2. Print the output for i3blocks (Full text, Short text)
echo "$ICON $CAPACITY% ($CYCLE_COUNT)"
echo "$ICON $CAPACITY%"

# 3. Change text color to red if battery is low and discharging
if [[ "$CAPACITY" -le 20 && "$STATUS" == "Discharging" ]]; then
    echo "#FF5555"
    
    # If the state file does NOT exist, send the notification
    if [[ ! -f "$STATE_FILE" ]]; then
        notify-send -u critical "Battery Low" "Plug in your charger! Capacity at ${CAPACITY}%."
        touch "$STATE_FILE" # Create the file so it doesn't notify again
    fi
else
    # If the battery is charging or above 20%, delete the state file to reset the trigger
    rm -f "$STATE_FILE"
fi
