#!/bin/bash

INTERFACE=wlp1s0
label="  "

# 1. Handle Clicks: If you left-click ($BLOCK_BUTTON = 1), send notification
if [[ "$BLOCK_BUTTON" -eq 1 ]]; then
    notify-send "$INTERFACE" "$(pcurl post citiez --silent)"
fi

# 2. Check Connection
SSID=$(iw dev "$INTERFACE" link | grep 'SSID' | awk '{$1=""; print $0}')

if [[ -z "$SSID" ]]; then
    echo "<span color='#FF0000'>$label Disconnected</span>"
elif curl -s --head --request GET http://www.google.com -m 1 | grep "200 OK" >/dev/null; then
    echo "<span color='#00FF00'>$label $SSID</span>"
else
    echo "<span color='#FFFF00'>$label $SSID</span>"
fi

