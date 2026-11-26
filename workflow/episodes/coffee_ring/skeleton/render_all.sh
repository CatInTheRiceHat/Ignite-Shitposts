#!/bin/zsh
# Render every gray skeleton clip headless. Usage: render_all.sh [version tag]
cd "$(dirname "$0")"
V=${1:-v1}
B=/Applications/Blender.app/Contents/MacOS/Blender
for c in 01a 01b 02a 02b 03 04 05; do
  $B -b --factory-startup --python render_clip.py -- $c ./$c-skeleton-$V.mp4 2>&1 | grep -E "RENDERED|Error|Traceback"
done
echo ALLDONE
