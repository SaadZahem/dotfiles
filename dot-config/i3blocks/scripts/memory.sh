#!/bin/bash

# 1. Right click to open htop
if [[ "$BLOCK_BUTTON" -eq 3 ]]; then
    terminator -e htop
fi

# 2. Get data using awk
# We calculate everything inside awk to ensure no shell formatting errors
read -r full_text used_percent < <(free -m | awk '/Mem:/ {printf "%.2fG/%.2fG %d", $3/1024, $2/1024, $3/$2*100}')

# 3. Output for i3blocks
echo "$full_text ($used_percent%)" # Line 1: Display
echo "$full_text" # Line 2: Short text

# 4. Color logic (Outputted as Line 3)
if [[ "$used_percent" -gt 80 ]]; then
    echo "#FFA500" # Orange if > 80%
elif [[ "$used_percent" -gt 90 ]]; then
    echo "#FF0000" # Red if > 90%
fi
