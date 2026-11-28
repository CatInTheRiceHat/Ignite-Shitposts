#!/bin/zsh
# 2026-11-27, after Elaine's notes on cut v5: ring low on Ring Sol everywhere, the fly-in passes under the banner, clips
# 1, 2 and 8 longer so every line has a pause after it. Skeletons, then the lettering passes that changed.
cd "$(dirname "$0")"
BL=/Applications/Blender.app/Contents/MacOS/Blender
run() { SKEL_FPS=24 $BL -b --factory-startup --python render_clip.py -- $1 "$PWD/$2" > logs/render_$1_r7.log 2>&1; echo "skeleton $1 exit $? $(grep -c Traceback logs/render_$1_r7.log)"; }
ovl() { rm -rf ../overlays/$1/seq; SKEL_FPS=24 MODE=ovlseq $BL -b --factory-startup --python render_clip.py -- $1 x.mp4 > logs/ovl_$1.log 2>&1; echo "lettering $1 exit $? $(ls ../overlays/$1/seq | wc -l)"; }
only() { rm -rf ../overlays/$1/seq_$3; SKEL_FPS=24 MODE=ovlseq OVLONLY=$2 SEQNAME=$3 OVLEND=${4:-9999} $BL -b --factory-startup --python render_clip.py -- $1 x.mp4 > logs/ovl_$1_$3.log 2>&1; echo "lettering $1 $3 exit $? $(ls ../overlays/$1/seq_$3 | wc -l)"; }
(run 1 01-skeleton-v3.mp4 & run 2 02-skeleton-v3.mp4 & run 6 06-skeleton-v4.mp4 & run 8 08-skeleton-v3.mp4 & wait)
(ovl 3 & ovl 6 & only 4 sign_moat moat & only 4 sign_walls walls & only 1 banner banner 60 & wait)
echo ALL DONE
