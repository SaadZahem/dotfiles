#!/usr/bin/env python3
"""Descriptive i3 keymap, in Python.

Configure i3 here, then run this file to (re)generate ``keymap.conf`` (which the
main i3 ``config`` ``include``s). Each ``km.bind(...)`` is translated to a
layout-independent ``bindcode`` when the key has a known keycode, or left as
``bindsym`` for named/layout-immune keys — see i3gen.py for the why and how.

Usage:
    ./i3config.py            # regenerate keymap.conf next to this file
"""

import sys
from pathlib import Path

from i3gen import Keymap

sys.dont_write_bytecode = True  # keep this config dir free of __pycache__
km = Keymap()

# --- i3 general controls ---------------------------------------------------
km.comment("i3 general controls")
# Reload/restart regenerate keymap.conf first, so editing this file and pressing
# the shortcut applies the change immediately.
km.bind("$mod+Shift+c", 'exec $noid "$config/i3/i3config.py && i3-msg reload"')
km.bind("$mod+Shift+r", 'exec $noid "$config/i3/i3config.py && i3-msg restart"')
km.bind(
    "$mod+Shift+Escape",
    "bar mode hide, exec \"i3-nagbar -t warning -m $msg-exit -B 'Yes, exit i3' 'i3-msg exit'\"",
)
km.bind(
    "$mod+x",
    'exec cd $config/actions && cat "$(ls | $config/i3/scripts/menu -p Actions $bar-bgcolor $bar-fgcolor)" | sh',
)
km.bind("$mod+Shift+x", "exec $config/i3/scripts/shiftx")

# --- workspace controls ----------------------------------------------------
km.blank()
km.comment("switch to workspace")
for i in range(1, 11):
    km.bind(f"$mod+{i % 10}", f"workspace number $ws{i}")

km.blank()
km.comment("move focused container to workspace")
for i in range(1, 11):
    km.bind(f"$mod+Shift+{i % 10}", f"move container to workspace number $ws{i}")

km.blank()
km.comment("other workspace controls")
km.bind("$mod+z", "workspace back_and_forth")
km.bind("$mod+Shift+z", "move container to workspace back_and_forth")
km.bind("$mod+Shift+bracketright", "workspace next")
km.bind("$mod+Shift+bracketleft", "workspace prev")

km.blank()
km.comment("renaming and running commands")
km.bind(
    "$mod+comma", "exec i3-input -P '(rename workspace) ' -F 'rename workspace to %s'"
)
km.bind("$mod+period", "exec i3-input -P '(create workspace) ' -F 'workspace %s'")
km.bind("$mod+F2", "exec i3-input -P '(rename window) ' -F 'exec set_title.sh \"%s\"'")
km.bind("$mod+slash", "exec i3-input -F '%s' -P \"i3-msg /> \"")
km.bind(
    "$mod+Shift+slash",
    'exec $noid i3-input -F \'exec notify-send "%s" "$(%s 2>&1)"\' -P "notify ?> "',
)

km.blank()
km.comment("vim-like marks")
km.bind("$mod+m", "exec i3-input -l 1 -F 'mark %s' -P '(mark) '")
km.bind("$mod+Shift+m", '[con_id="__focused__"] unmark')
km.bind(
    "$mod+apostrophe",
    "exec i3-input -l 1 -F '[con_mark=\"%s\"] focus' -P '(goto mark) '",
)
km.bind(
    "$mod+Shift+apostrophe",
    "exec i3-input -l 1 -F 'swap container with mark %s' -P '(swap with mark) '",
)
km.bind("$mod+q", '[con_mark="q"] focus')

# --- layout controls -------------------------------------------------------
km.blank()
km.comment("change container layout (stacked, tabbed, toggle split)")
km.bind("$mod+w", "layout tabbed")
km.bind("$mod+e", "layout toggle split")
km.bind("$mod+Shift+e", "split toggle")
km.bind("$mod+s", "layout stacking")
km.bind("$mod+Control+h", "split h")
km.bind("$mod+Control+v", "split v")

km.blank()
km.comment("fullscreen, floating, and sticky")
km.bind("$mod+f", "fullscreen toggle")
km.bind("$mod+Shift+f", "floating toggle")
km.bind("$mod+Shift+t", "sticky toggle")

km.blank()
km.comment("scratchpad")
km.bind("$mod+minus", "scratchpad show")
km.bind("$mod+Shift+minus", "move scratchpad")

km.blank()
km.comment("toggle bar visibility")
km.bind("$mod+Shift+b", "bar mode toggle")

km.blank()
km.comment("show window title")
km.bind("$mod+t", "border normal")
km.bind("$mod+Shift+q", "border pixel")

# --- window controls -------------------------------------------------------
km.blank()
km.comment("change focus")
km.bind("$mod+h", "focus left")
km.bind("$mod+j", "focus down")
km.bind("$mod+k", "focus up")
km.bind("$mod+l", "focus right")
km.bind("$mod+semicolon", "focus mode_toggle")
km.blank()
km.bind("$mod+Left", "focus left")
km.bind("$mod+Down", "focus down")
km.bind("$mod+Up", "focus up")
km.bind("$mod+Right", "focus right")
km.blank()
km.bind("$mod+p", "focus parent")
km.bind("$mod+Shift+p", "focus child")
km.blank()
km.bind("$mod+bracketright", "focus next")
km.bind("$mod+bracketleft", "focus prev")
km.bind("$mod+Tab", "focus next")
km.bind("$mod+Shift+Tab", "focus prev")

km.blank()
km.comment("move focused window")
km.bind("$mod+Shift+h", "move left")
km.bind("$mod+Shift+j", "move down")
km.bind("$mod+Shift+k", "move up")
km.bind("$mod+Shift+l", "move right")
km.blank()
km.bind("$mod+Shift+Left", "move left")
km.bind("$mod+Shift+Down", "move down")
km.bind("$mod+Shift+Up", "move up")
km.bind("$mod+Shift+Right", "move right")

km.blank()
km.comment("kill focused window")
km.bind("$mod+Shift+w", "kill")
km.bind("$mod+Escape", "kill")
km.bind(
    "$mod+v", "exec i3-input -l 1 -F '[workspace=\"%s\"] kill' -P '(kill workspace) '"
)

# --- start applications ----------------------------------------------------
km.blank()
km.comment("common applications")
km.bind("$mod+Return", "exec i3-sensible-terminal")
km.bind("$mod+Shift+Return", 'exec i3-sensible-terminal -T "FloatShell"')
km.bind(
    "$mod+d",
    "exec $noid $config/i3/scripts/menu -c dmenu_run -p Run $bar-bgcolor $bar-fgcolor &> $home/.var/dmenu.log",
)
km.bind("$mod+Shift+d", "exec $noid networkmanager_dmenu")
km.bind(
    "$mod+c",
    "exec j4-dmenu-desktop --dmenu=\"$config/i3/scripts/menu -p Run '$bar-bgcolor' '$bar-fgcolor'\" &> $home/.var/dmenu.log",
)

km.blank()
km.comment("launch custom Unicode grid picker")
km.bind("$mod+u", "exec $noid rofi-unicode")

km.blank()
km.comment("screenshot tools")
km.bind("Print", "exec prtsc screen")
km.bind("$mod+Print", "exec prtsc window")
km.bind("$mod+Shift+s", "exec prtsc part")

km.blank()
km.comment("toggle CopyQ clipboard manager")
km.bind("$mod+Shift+v", 'exec $noid "test $(copyq toggle) = false && i3 kill"')

km.blank()
km.comment("pop up the most recent missed notification")
km.bind("$mod+n", "exec $noid dunstctl history-pop")
km.bind("$mod+Shift+n", "exec dunstctl set-paused toggle && pkill -RTMIN+11 i3blocks")

km.blank()
km.comment("launch boomer (zoomit alternative)")
km.bind("$mod+grave", "exec $noid boomer")

km.blank()
km.comment("launch peek (screen recorder)")
km.bind("$mod+$alt+r", "exec peek")

# --- modes -----------------------------------------------------------------
km.blank()
km.comment("resize mode")
with km.mode("resize"):
    km.comment("left/right shrink/grow width; up/down shrink/grow height")
    km.bind("h", "resize shrink width 10 px or 10 ppt")
    km.bind("j", "resize grow height 10 px or 10 ppt")
    km.bind("k", "resize shrink height 10 px or 10 ppt")
    km.bind("l", "resize grow width 10 px or 10 ppt")
    km.blank()
    km.comment("same bindings, but for the arrow keys")
    km.bind("Left", "resize shrink width 10 px or 10 ppt")
    km.bind("Down", "resize grow height 10 px or 10 ppt")
    km.bind("Up", "resize shrink height 10 px or 10 ppt")
    km.bind("Right", "resize grow width 10 px or 10 ppt")
    km.blank()
    km.bind("b", 'mode "border"')
    km.blank()
    km.comment("back to normal: Enter or Escape or $mod+r")
    km.bind("Return", 'mode "default"')
    km.bind("Escape", 'mode "default"')
    km.bind("$mod+r", 'mode "default"')
km.bind("$mod+r", 'mode "resize"')

km.blank()
km.comment("border mode — manipulate borders of any window")
with km.mode("border"):
    km.comment("quick border settings")
    km.bind("t", "border normal")
    km.bind("0", "border none")
    km.blank()
    km.comment("adjusting border width")
    for n in range(1, 10):
        km.bind(str(n), f"border pixel {n}")
    km.blank()
    km.comment("controlling gaps")
    km.bind("i", "gaps inner current toggle 8")
    km.bind("o", "gaps outer current toggle 8")
    km.blank()
    km.comment("controlling status bar")
    km.bind("q", "bar mode dock")
    km.bind("a", "bar mode hide")
    km.bind("z", "bar mode invisible")
    km.blank()
    km.comment("control window title")
    km.bind("w", "title_window_icon toggle 8")
    km.bind("x", "title_format $title-bold-verbose")
    km.bind("s", "title_format $title-bold")
    km.blank()
    km.comment("center dialog")
    km.bind("c", "move position center")
    km.blank()
    km.bind("r", 'mode "resize"')
    km.blank()
    km.comment("exit to default mode")
    km.bind("Return", 'mode "default"')
    km.bind("Escape", 'mode "default"')
    km.bind("$mod+b", 'mode "default"')
km.bind("$mod+b", 'mode "border"')

km.blank()
km.comment("gaming automation mode")
with km.mode("auto"):
    km.bind("p", "exec \"xdotool key --window '$(xdotool getactivewindow)' Pause\"")
    km.bind("q", "exec xdotool key --delay 50 Pause Pause")
    km.bind(
        "i",
        'exec $noid i3-input -F \'exec notify-send "%s" "$(xdotool key --delay %s 2>&1)"\' -P "notify ?> "',
    )
    km.blank()
    km.bind("Return", 'mode "default"')
    km.bind("Escape", 'mode "default"')
    km.bind("$mod+a", 'mode "default"')
km.bind("$mod+a", 'mode "auto"')


if __name__ == "__main__":
    out = Path(__file__).with_name("keymap.conf")
    km.write(out, source="i3config.py")
    print(f"wrote {out} ({len(km._lines)} lines)")
