#!/usr/bin/env bash

# Automatically detect the primary battery (BAT0, BAT1, etc.)
BAT_DIR=$(find /sys/class/power_supply -name "BAT*" | head -n 1)

if [ -z "$BAT_DIR" ]; then
    echo "No battery detected in /sys/class/power_supply" >&2
    exit 1
fi

LOG_FILE="$HOME/.var/battery_log.csv"

# Read sysfs attributes safely (returns 0 or N/A if missing)
read_val() {
    local file="$BAT_DIR/$1"
    if [ -f "$file" ]; then
        cat "$file"
    else
        echo "0"
    fi
}

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
STATUS=$(read_val "status")
CAPACITY=$(read_val "capacity")       # percentage (0-100)
CYCLE_COUNT=$(read_val "cycle_count") # recharge cycles

# Resolve energy or charge attributes depending on hardware driver
FULL=$(read_val "energy_full")
FULL_DESIGN=$(read_val "energy_full_design")

if [ "$FULL" -eq 0 ] 2>/dev/null; then
    FULL=$(read_val "charge_full")
    FULL_DESIGN=$(read_val "charge_full_design")
fi

# Calculate health percentage: (full / full_design) * 100
if [ -n "$FULL" ] && [ -n "$FULL_DESIGN" ] && [ "$FULL_DESIGN" -gt 0 ] 2>/dev/null; then
    HEALTH_PCT=$(awk -v f="$FULL" -v fd="$FULL_DESIGN" 'BEGIN { printf "%.2f", (f / fd) * 100 }')
else
    HEALTH_PCT="N/A"
fi

# Initialize CSV header if the log file does not exist
if [ ! -f "$LOG_FILE" ]; then
    echo "timestamp,level_pct,status,cycle_count,full,full_design,health_pct" >> "$LOG_FILE"
fi

# Append data row
echo "$TIMESTAMP,$CAPACITY%,$STATUS,$CYCLE_COUNT,$FULL,$FULL_DESIGN,$HEALTH_PCT%" >> "$LOG_FILE"
