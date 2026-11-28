#!/bin/zsh
# 2026-11-27: the ring right down at Ring Sol's feet, no plan board in clips 1, 7 and 8, clip 8's wide view further back.
cd "$(dirname "$0")"
BL=/Applications/Blender.app/Contents/MacOS/Blender
run() { SKEL_FPS=24 $BL -b --factory-startup --python render_clip.py -- $1 "$PWD/$2" > logs/render_$1_r8.log 2>&1; echo "skeleton $1 exit $? $(grep -c Traceback logs/render_$1_r8.log)"; }
ovl() { rm -rf ../overlays/$1/seq; SKEL_FPS=24 MODE=ovlseq $BL -b --factory-startup --python render_clip.py -- $1 x.mp4 > logs/ovl_$1.log 2>&1; echo "lettering $1 exit $? $(ls ../overlays/$1/seq | wc -l)"; }
only() { rm -rf ../overlays/$1/seq_$3; SKEL_FPS=24 MODE=ovlseq OVLONLY=$2 SEQNAME=$3 $BL -b --factory-startup --python render_clip.py -- $1 x.mp4 > logs/ovl_$1_$3.log 2>&1; echo "lettering $1 $3 exit $? $(ls ../overlays/$1/seq_$3 | wc -l)"; }
(run 1 01-skeleton-v4.mp4 & run 2 02-skeleton-v4.mp4 & run 6 06-skeleton-v5.mp4 & run 7 07-skeleton-v7.mp4 & run 8 08-skeleton-v4.mp4 & wait)
(ovl 6 & only 1 banner banner & only 5 clock_board judging & wait)
echo ALL DONE
