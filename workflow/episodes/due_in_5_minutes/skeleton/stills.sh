#!/bin/zsh
# Check stills: stills.sh <out_dir> <clip> <frames> [<clip> <frames> ...]   (lettering planes shown)
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT=$1; shift
while [ $# -gt 1 ]; do
  SHOWOVL=1 $B -b --factory-startup --python render_clip.py -- $1 - $2 "$OUT" 2>&1 | grep -E "STILLS|Error|Traceback|  File|line [0-9]"
  shift 2
done
