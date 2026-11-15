#!/bin/sh
# Build a SILE document the way a PDF viewer can cope with.
#
# Usage:  sil-sync.sh [sile options] document.sil
#
# SILE (via libtexpdf) writes the PDF where it was asked to as it goes, so for
# the whole duration of the run the file on disk is truncated and half written.
# A viewer watching that file (Zathura, Evince, ...) re-reads it, finds no PDF
# at all, and logs things like "mupdf: format error: cannot find startxref".
#
# This wrapper renders into a temporary directory next to the document, then
# moves the finished PDF (and its SyncTeX file) over the old one with rename(2),
# which is atomic: the viewer only ever sees the previous complete file or the
# new complete file.
#
# Put the SILE you want to use in $SILE if it is not on the PATH, e.g.
#   SILE=/usr/local/bin/sile sil-sync.sh --synctex hello.sil

set -e

doc=
for arg in "$@"; do
   case $arg in
      -*)
         ;;
      *)
         doc=$arg
         ;;
   esac
done

if [ -z "$doc" ] || [ ! -f "$doc" ]; then
   printf 'usage: %s [sile options] document.sil\n' "$0" >&2
   exit 2
fi

sile=${SILE:-sile}
dir=$(cd "$(dirname "$doc")" && pwd)
base=$(basename "$doc")
name=${base%.*}

# Same directory, hence same file system: rename(2) cannot fail with EXDEV.
tmp=$(mktemp -d "$dir/.sile-build.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

"$sile" -o "$tmp/$name.pdf" "$@" || exit

mv -f "$tmp/$name.pdf" "$dir/$name.pdf"
if [ -f "$tmp/$name.synctex.gz" ]; then
   mv -f "$tmp/$name.synctex.gz" "$dir/$name.synctex.gz"
elif [ -f "$tmp/$name.synctex" ]; then
   mv -f "$tmp/$name.synctex" "$dir/$name.synctex"
fi

printf '%s: rebuilt\n' "$dir/$name.pdf" >&2
