source ~/.bashrc

# Setting up autocompletion
autoload -Uz compinit
compinit

# Source the plugins we installed via pacman
# 1. Autosuggestions (shows ghost text of past commands)
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# 2. Syntax Highlighting (turns commands green if valid, red if invalid)
# Note: This must always be the very last plugin sourced!
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# Initialize the Starship prompt
eval "$(starship init zsh)"

# History
HISTFILE=~/.zsh_history
HISTSIZE=999999
SAVEHIST=$HISTSIZE

## History Options
setopt EXTENDED_HISTORY          # Write the history file in the ':start:elapsed;command' format.
setopt HIST_EXPIRE_DUPS_FIRST    # Expire a duplicate event first when trimming history.
setopt HIST_FIND_NO_DUPS         # Do not display a previously found event.
setopt HIST_IGNORE_ALL_DUPS      # Delete an old recorded event if a new event is a duplicate.
setopt HIST_IGNORE_DUPS          # Do not record an event that was just recorded again.
setopt HIST_IGNORE_SPACE         # Do not record an event starting with a space.
setopt HIST_SAVE_NO_DUPS         # Do not write a duplicate event to the history file.
setopt SHARE_HISTORY             # Share history between all sessions.
