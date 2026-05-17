#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias tree='tree -C'
PS1='[\u@\h \W]\$ '

export PATH="$HOME/.local/bin:$PATH"
export EDITOR=/usr/bin/vim
export TERMINAL=terminator
export WM=i3

# Locations I use
export WINEPREFIX="$HOME/.wine"
export C="$WINEPREFIX/drive_c/"
export TELEGRAM_DESKTOP="$HOME/Downloads/Telegram Desktop/"

# Starting window manager of choice
alias si3='WM=i3 startx'
alias splasma='WM=plasma startx'
alias sxfce='WM=xfce startx'

# Personalized aliases
alias edit='$EDITOR $1'
alias tt=taskwarrior-tui
alias restore3='i3-resurrect restore -w 3'
alias pcurlloop='pcurl post citiez -l 6 &>/dev/null &'
alias until='while true; do $1 && break; done'
alias forever='while true; do $2; sleep $1; done'
