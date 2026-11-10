#!/bin/bash
# Full build of one tutorial part with the signature ending: stage frames (4 workers), ending composite, mix, encode.
# Usage: build_part.sh <part dir> <output mp4 name>
set -e
D=$1; OUT=$2; KIT=$(dirname "$(readlink -f "$0")")
cd "$D"
N=$(node -e "global.window={};eval(require('fs').readFileSync('stage/timeline.js','utf8'));console.log(Math.round(window.TL.T*window.TL.fps))")
Q=$(( (N + 3) / 4 ))
rm -rf frames_c && mkdir frames_c
node render.js range 0 $Q frames_c > rc_0.log 2>&1 &
node render.js range $Q $((2*Q)) frames_c > rc_1.log 2>&1 &
node render.js range $((2*Q)) $((3*Q)) frames_c > rc_2.log 2>&1 &
node render.js range $((3*Q)) $N frames_c > rc_3.log 2>&1 &
wait
echo "$D rendered $(ls frames_c | wc -l) of $N"
python3 "$KIT/compose_kit.py" frames "$D" "$D/frames_c" 4 | tail -1
python3 "$KIT/mix_consistent.py" "$D"
FPS=$(python3 -c "import json;print(json.load(open('kitcues.json'))['fps'])")
ffmpeg -v error -y -framerate $FPS -i frames_c/f%05d.jpg -i mix.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart -shortest "$OUT"
echo "$D encoded $OUT $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
