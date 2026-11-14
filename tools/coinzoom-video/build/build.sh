#!/bin/bash
# Full build: timeline, frames (4 workers), the one signature mix, encode.  Usage: ./build.sh <out.mp4>
set -e
cd "$(dirname "$(readlink -f "$0")")"; . ./env.sh
python3 make_tl.py > tl.log
N=$(python3 -c "import json;t=json.load(open('timeline.json'));print(round(t['T']*t['fps']))"); Q=$(( (N + 3) / 4 ))
rm -rf frames && mkdir frames
for i in 0 1 2 3; do a=$((i*Q)); b=$(( (i+1)*Q < N ? (i+1)*Q : N )); python3 render.py range $a $b frames > r_$i.log 2>&1 & done
wait
echo "rendered $(ls frames | wc -l) of $N"
python3 mix_consistent.py "$PWD"
ffmpeg -v error -y -framerate 30 -i frames/f%05d.jpg -i mix.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest "$1"
echo "encoded $1 $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1") s"
