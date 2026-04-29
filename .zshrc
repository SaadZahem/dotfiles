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
