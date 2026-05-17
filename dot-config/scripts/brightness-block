#!/bin/bash

# The -m flag formats the output as a comma-separated list
# awk extracts the 4th column, which is the exact percentage (e.g., 50%)
percent=$(brightnessctl -m | awk -F, '{print $4}')

echo "BRI $percent"
