#!/bin/zsh
# Render every skeleton clip (v2: the dressed beach), then every lettering pass. Usage: ./render_all.sh
cd "$(dirname "$0")"
BL=/Applications/Blender.app/Contents/MacOS/Blender
run() { SKEL_FPS=24 $BL -b --factory-startup --python render_clip.py -- $1 "$PWD/0$1-skeleton-v2.mp4" > logs/render_$1.log 2>&1; echo "skeleton $1 exit $?"; }
ovl() { SKEL_FPS=24 MODE=ovlseq $BL -b --factory-startup --python render_clip.py -- $1 x.mp4 > logs/ovl_$1.log 2>&1; echo "lettering $1 exit $? $(ls ../overlays/$1/seq 2>/dev/null | wc -l) frames"; }
(run 2 & run 1 & run 3 & run 4 & wait)
(run 5 & run 6 & run 7 & run 8 & wait)
(ovl 1 & ovl 2 & ovl 3 & ovl 4 & wait)
(ovl 5 & ovl 6 & ovl 7 & ovl 8 & wait)
echo ALL DONE
