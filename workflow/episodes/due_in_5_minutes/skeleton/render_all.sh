#!/bin/zsh
# Render gray-pass clips headless. Usage: render_all.sh <version tag> [clip numbers...]
cd "$(dirname "$0")"
V=$1; shift
B=/Applications/Blender.app/Contents/MacOS/Blender
if [ $# -eq 0 ]; then set -- 1 2 3 4 5 6 7 8 9; fi
for c in "$@"; do
  $B -b --factory-startup --python render_clip.py -- $c ./0$c-skeleton-$V.mp4 2>&1 | grep -E "RENDERED|Error|Traceback"
done
echo ALLDONE
