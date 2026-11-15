#!/usr/bin/env bash

WID=$(xdotool getwindowfocus 2>/dev/null)
test -z "$WID" && exit 1

PID=$(xdotool getwindowpid "$WID" 2>/dev/null)
test -z "$PID" && exit 1

STATE=$(ps -o state= -p "$PID" | tr -d ' ')
if [[ "$STATE" == *"T"* ]]
then
    kill -CONT "$PID"
    xprop -id "$WID" -f _NET_WM_WINDOW_OPACITY 32c -set _NET_WM_WINDOW_OPACITY 4294967295
    notify-send "Unpause" "$WID $PID $STATE"
else
    kill -STOP "$PID"
    xprop -id "$WID" -f _NET_WM_WINDOW_OPACITY 32c -set _NET_WM_WINDOW_OPACITY 2147483648
    notify-send "Pause" "$WID $PID $STATE"
fi
