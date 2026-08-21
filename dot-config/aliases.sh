alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias tree='tree -C'

alias edit='$EDITOR $1'
alias open=xdg-open
alias summon=i3-summon

alias hh="vim + ~/.zsh_history"
alias pp="uv version --bump"
alias tt=taskwarrior-tui
alias vv='source .venv/bin/activate'

rr() {
    file=/tmp/rr
    ranger --choosedir=$file $*
    dir=$(cat $file)
    cd $dir
    rm $file
}
pcurlloop() {
    while true
    do
        date
        pcurl -s
        echo
        sleep ${1:-6}
    done
}
orphans(){
    for pack in $(pacman -Qdtq)
    do
        pacman -Ss "^$pack$"
    done
}
showpack() {
    pamac info $1 | rg "Required|Optional|Depends"
}
