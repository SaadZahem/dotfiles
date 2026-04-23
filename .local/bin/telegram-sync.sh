#!/bin/bash

TELEGRAM_DIR="$HOME/Downloads/Telegram Desktop"
PDF_DIR="$HOME/Documents/Data/telegram-sync/PDFs"
M4A_DIR="$HOME/Documents/Data/telegram-sync/M4As"
STAMP_FILE="$HOME/.local/state/telegram_sync.stamp"

mkdir -p "$PDF_DIR" "$M4A_DIR" "${STAMP_FILE%/*}"

FIND_ARGS=()
[[ -f "$STAMP_FILE" ]] && FIND_ARGS=("-newer" "$STAMP_FILE")

find "$TELEGRAM_DIR" -type f \( -iname "*.pdf" -o -iname "*.m4a" \) "${FIND_ARGS[@]}" -print0 | while IFS= read -r -d $'\0' file; do
    filename=$(basename "$file")
    if [[ "${file,,}" == *.pdf ]]; then
        ln -sf "$file" "$PDF_DIR/$filename"
        notify-send "telegram-sync" "linked pdf: $file"
    elif [[ "${file,,}" == *.m4a ]]; then
        ln -sf "$file" "$M4A_DIR/$filename"
        notify-send "telegram-sync" "linked audio: $file"
    fi
done

touch "$STAMP_FILE"
