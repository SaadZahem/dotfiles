#!/usr/bin/env sh

TELEGRAM_DIR="$HOME/Downloads/Telegram Desktop"
TGSYNC_DIR="$HOME/mnt/tgsync"
STAMP_FILE="$HOME/.local/state/telegram_sync.stamp"

mkdir -p "$PDF_DIR" "$M4A_DIR" "${STAMP_FILE%/*}"

FIND_ARGS=()
[[ -f "$STAMP_FILE" ]] && FIND_ARGS=("-newer" "$STAMP_FILE")

find "$TELEGRAM_DIR" -type f "${FIND_ARGS[@]}" -print0 | while IFS= read -r -d $'\0' file
do
    suffix=${file##*.}
    name=$(basename "$file" ".$suffix")

    ln -sf "$file" "$TGSYNC_DIR/$suffix/$name"
    if [[ "$suffix" =~ "mp3|m4a" ]]; then
        ln -sf "$file" "$TGSYNC_DIR/audio/$name"
    fi

    notify-send "Telegram Sync" "Linked $suffix: $file"
done

touch "$STAMP_FILE"
