#!/usr/bin/env bash

# hardcoded to the only interface that supports hotspot on my machine
INTERFACE=${INTERFACE:-wlp1s0}

case "$1" in
    (on)
        nmcli device wifi hotspot ifname $INTERFACE ssid laplab password ${INTERFACE}67 || exit 1
        notify-send 'Hotspot enabled' "$INTERFACE"
        ;;
    (off)
        nmcli connection | awk "/^Hotspot.*$INTERFACE/ {print \$2}" | xargs nmcli connection down || exit 1
        notify-send 'Hotspot disabled' "$INTERFACE"
        ;;
esac
