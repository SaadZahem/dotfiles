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

# Full video capped at 360p
yt-low() {
  yt-dlp \
    --extractor-args "youtube:player-client=web,mweb" \
    -f "bv*[ext=mp4][height<=360]+ba[ext=m4a]/b[ext=mp4][height<=360]/b[height<=360]" \
    --merge-output-format mp4 \
    "$1"
}

# Slice at max/native quality: yt-cut <URL> <START-END>
# Example: yt-cut "https://..." "01:30-03:45"
yt-cut() {
  yt-dlp \
    --extractor-args "youtube:player-client=web,mweb" \
    -f "bv*+ba/b" \
    --merge-output-format mp4 \
    --download-sections "*$2" \
    --force-keyframes-at-cuts \
    "$1"
}
