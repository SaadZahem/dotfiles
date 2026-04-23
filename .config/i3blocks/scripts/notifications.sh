#!/bin/bash
# vim: et ts=4 sw=4 sts=4

[ "$BLOCK_BUTTON" == "1" ] && dunstctl set-paused toggle

if [ "$(dunstctl is-paused)" == "false" ]; then
    echo "NOTIF ON"
else
    echo "NOTIF OFF"
fi
