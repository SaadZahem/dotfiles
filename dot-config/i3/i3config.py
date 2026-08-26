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
# i3 general controls
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


def workspace():
    # switch to workspace
    for i in range(1, 11):
        km.bind(f"$mod+{i % 10}", f"workspace number $ws{i}")

    # move focused container to workspace
    for i in range(1, 11):
        km.bind(
            f"$mod+Shift+{i % 10}", f"mark q, move container to workspace number $ws{i}"
        )

    # other workspace controls
    km.bind("$mod+z", "workspace back_and_forth")
    km.bind("$mod+Shift+z", "move container to workspace back_and_forth")
    km.bind("$mod+Shift+bracketright", "workspace next")
    km.bind("$mod+Shift+bracketleft", "workspace prev")

    # renaming and running commands
    km.bind(
        "$mod+comma",
        "exec i3-input -P '(rename workspace) ' -F 'rename workspace to %s'",
    )
    km.bind("$mod+period", "exec i3-input -P '(create workspace) ' -F 'workspace %s'")
    km.bind(
        "$mod+F2", "exec i3-input -P '(rename window) ' -F 'exec set_title.sh \"%s\"'"
    )
    km.bind("$mod+slash", "exec i3-input -F '%s' -P \"i3-msg /> \"")
    km.bind(
        "$mod+Shift+slash",
        'exec $noid i3-input -F \'exec notify-send "%s" "$(%s 2>&1)"\' -P "notify ?> "',
    )

    # vim-like marks
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


def layout():
    # change container layout (stacked, tabbed, toggle split)
    km.bind("$mod+w", "layout tabbed")
    km.bind("$mod+e", "layout toggle split")
    km.bind("$mod+Shift+e", "split toggle")
    km.bind("$mod+s", "layout stacking")
    km.bind("$mod+Control+h", "split h")
    km.bind("$mod+Control+v", "split v")

    # fullscreen, floating, and sticky
    km.bind("$mod+f", "fullscreen toggle")
    km.bind("$mod+Shift+f", "floating toggle")
    km.bind("$mod+Shift+t", "sticky toggle")
    km.bind(
        "$mod+$alt+f",
        "resize set width 1920, resize set height 1080, move position center",
    )

    # scratchpad
    km.bind("$mod+minus", "scratchpad show")
    km.bind("$mod+Shift+minus", "move scratchpad")

    # toggle bar visibility
    km.bind("$mod+Shift+b", "bar mode toggle")
    km.bind("$mod+$alt+b", "bar mode invisible")

    # show window title
    km.bind("$mod+t", "border normal")
    km.bind("$mod+Shift+q", "border pixel")


# --- window controls -------------------------------------------------------


def window():
    # change focus
    focus = dict(
        left=["h", "Left"],
        down=["j", "Down"],
        up=["k", "Up"],
        right=["l", "Right"],
        parent=["p"],
        child=["Shift+p"],
        next=["bracketright", "Tab"],
        prev=["bracketleft", "Shift+Tab"],
        mode_toggle=["semicolon"],
    )
    for name, keys in focus.items():
        for key in keys:
            km.bind(f"$mod+{key}", f"focus {name}")

    # move focused window
    move = dict(
        left=["h", "Left"],
        down=["j", "Down"],
        up=["k", "Up"],
        right=["l", "Right"],
    )
    for name, keys in move.items():
        for key in keys:
            km.bind(f"$mod+Shift+{key}", f"move {name}")

    # kill focused window
    km.bind("$mod+Shift+w", "kill")
    km.bind("$mod+Escape", "kill")
    km.bind(
        "$mod+v",
        "exec i3-input -l 1 -F '[workspace=\"%s\"] kill' -P '(kill workspace) '",
    )


# --- start applications ----------------------------------------------------


def application():
    # common applications
    km.bind("$mod+Return", "exec i3-sensible-terminal")
    km.bind("$mod+Shift+Return", 'exec i3-sensible-terminal -T "FloatShell"')
    km.bind(
        "$mod+d",
        "exec $noid $config/i3/scripts/menu -c dmenu_run -p Run "
        "$bar-bgcolor $bar-fgcolor &> $home/.var/dmenu.log",
    )
    km.bind("$mod+c", "exec $noid networkmanager_dmenu")
    km.bind(
        "$mod+Shift+d",
        'exec j4-dmenu-desktop --dmenu="$config/i3/scripts/menu -p Run '
        "'$bar-bgcolor' '$bar-fgcolor'\" &> $home/.var/dmenu.log",
    )

    # download a youtube video from the copied url
    km.bind(
        "$mod+y",
        'exec $noid bash -c \'yt-dlp --recode-video mp4 -P ~/Downloads "$(xclip -o -selection clipboard)"'
        " &>~/.var/yt-dlp.log"
        " && notify-send yt-dlp 'Download finished!' || notify-send -u critical yt-dlp 'Download failed!'",
        "--release",
    )

    # launch custom Unicode grid picker
    km.bind("$mod+u", "exec $noid rofi-unicode")

    # screenshot tools
    km.bind("Print", "exec prtsc screen")
    km.bind("$mod+Print", "exec prtsc window")
    km.bind("$mod+Shift+s", "exec prtsc part")

    # toggle CopyQ clipboard manager
    km.bind(
        "$mod+Shift+v",
        'exec $noid "test $(copyq toggle) = false && i3-msg [class=copyq] kill"',
    )

    # pop up the most recent missed notification
    km.bind("$mod+n", "exec $noid dunstctl history-pop")
    km.bind(
        "$mod+Shift+n", "exec dunstctl set-paused toggle && pkill -RTMIN+11 i3blocks"
    )

    # launch boomer (zoomit alternative)
    km.bind("$mod+grave", "exec $noid boomer")

    # launch peek (screen recorder)
    km.bind("$mod+$alt+r", "exec peek")


# --- modes -----------------------------------------------------------------


def resize():
    with km.mode("resize", "$mod+r"):
        # left/right shrink/grow width; up/down shrink/grow height
        km.bind("h", "resize shrink width 10 px or 10 ppt")
        km.bind("j", "resize grow height 10 px or 10 ppt")
        km.bind("k", "resize shrink height 10 px or 10 ppt")
        km.bind("l", "resize grow width 10 px or 10 ppt")

        # same bindings, but for the arrow keys
        km.bind("Left", "resize shrink width 10 px or 10 ppt")
        km.bind("Down", "resize grow height 10 px or 10 ppt")
        km.bind("Up", "resize shrink height 10 px or 10 ppt")
        km.bind("Right", "resize grow width 10 px or 10 ppt")

        km.bind("b", 'mode "border"')

        # back to normal: Enter or Escape or $mod+r
        km.bind("Return", 'mode "default"')
        km.bind("Escape", 'mode "default"')


def border():
    with km.mode("border", "$mod+b"):
        # quick border settings
        km.bind("t", "border normal")
        km.bind("0", "border none")

        # adjusting border width
        for n in range(1, 10):
            km.bind(str(n), f"border pixel {n}")

        # controlling gaps
        km.bind("i", "gaps inner current toggle 8")
        km.bind("o", "gaps outer current toggle 8")

        # controlling status bar
        km.bind("q", "bar mode dock")
        km.bind("a", "bar mode hide")
        km.bind("z", "bar mode invisible")

        # control window title
        km.bind("w", "title_window_icon toggle 8")
        km.bind("x", "title_format $title-bold-verbose")
        km.bind("s", "title_format $title-bold")

        # center dialog
        km.bind("c", "move position center")

        km.bind("r", 'mode "resize"')

        # exit to default mode
        km.bind("Return", 'mode "default"')
        km.bind("Escape", 'mode "default"')


def game():
    with km.mode("claw"):
        workspace()
        layout()
        window()

        km.bind("v", "exec xdotool key Pause", "--release")
        km.bind("c", "exec xdotool key --delay 40 Pause Pause", "--release")
        km.bind("b", "exec xdotool key Pause Space", "--release")
        km.bind("z", "exec xdotool key F1", "--release")

        km.bind("$mod+g", "mode default")
    km.bind(
        "$mod+g",
        'exec $noid test "$(xdotool getactivewindow getwindowclassname)" = "claw.exe"'
        " && i3-msg mode claw",
    )


def main():
    workspace()
    layout()
    window()
    application()
    resize()
    border()
    game()

    out = Path(__file__).with_name("keymap.conf")
    km.write(out, source="i3config.py")
    print(f"wrote {out} ({len(km._lines)} lines)")


if __name__ == "__main__":
    main()
