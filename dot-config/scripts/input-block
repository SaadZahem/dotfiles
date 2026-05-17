#!/bin/bash

# 1. If clicked via mouse OR triggered by Win+Space shortcut
if [[ "$BLOCK_BUTTON" -eq 1 || "$1" == "toggle" ]]; then
    CURRENT_LAYOUT=$(setxkbmap -query | awk '/layout:/ {print $2}')
    
    # Toggle and apply your specific variants
    if [[ "$CURRENT_LAYOUT" == "us" ]]; then
        setxkbmap -model pc105 -layout ara -variant digits
    else
        setxkbmap -model pc105 -layout us
    fi
fi

# 2. Print the current layout to the status bar
FINAL_LAYOUT=$(setxkbmap -query | awk '/layout:/ {print $2}')
echo "⌨ ${FINAL_LAYOUT^^}"
