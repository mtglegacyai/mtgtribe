#!/bin/bash
# Full build of one narrated CoinZoom clip: timeline, frames (4 workers), the one signature mix, encode.
# Usage: engine/build.sh <video dir> <out.mp4>    (the video dir holds make_tl.py, lines.json, words.json and the clip's
# frames in src720/ or src1080/; run engine/fetch_bank.sh once, then <video dir>/lines.py and engine/words.py <video dir>)
set -e
E=$(dirname "$(readlink -f "$0")"); V=$(readlink -f "$1"); OUT=$(readlink -f "$(dirname "$2")")/$(basename "$2")
. "$E/env.sh"; cd "$V"
python3 make_tl.py > tl.log
N=$(python3 -c "import json;t=json.load(open('timeline.json'));print(round(t['T']*t['fps']))"); Q=$(( (N + 3) / 4 ))
rm -rf frames && mkdir frames
for i in 0 1 2 3; do a=$((i*Q)); b=$(( (i+1)*Q < N ? (i+1)*Q : N )); python3 "$E/render.py" "$V" range $a $b frames > r_$i.log 2>&1 & done
wait
echo "rendered $(ls frames | wc -l) of $N"
python3 "$E/mix_consistent.py" "$V"
ffmpeg -v error -y -framerate 30 -i frames/f%05d.jpg -i mix.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest "$OUT"
echo "encoded $OUT $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT") s"
