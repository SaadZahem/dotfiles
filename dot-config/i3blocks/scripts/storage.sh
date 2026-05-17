#!/bin/bash

# Read the target directory passed from the i3blocks config
TARGET="$1"

# Handle the right mouse click (Button 1)
if [[ "$BLOCK_BUTTON" -eq 3 ]]; then
    [[ "$TARGET" == "/home" ]] && TARGET=$HOME
    setsid thunar "$TARGET" >/dev/null
fi

# Run df on the target partition and format the output
df -h "$TARGET" | awk '/\// {print $4 "/" $2}'

