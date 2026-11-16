#!/bin/bash
# Re-encode a finished build from its frames and mix (AAC 256k), then check loudness and peak.
set -e
D=$1; OUT=$2; cd "$D"; FPS=$(python3 -c "import json;print(json.load(open('kitcues.json'))['fps'])")
ffmpeg -v error -y -framerate $FPS -i frames_c/f%05d.jpg -i mix.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart -shortest "$OUT"
echo "$D $OUT $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
ffmpeg -v info -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2 | tr -s ' ' | tr '\n' ' '
ffmpeg -v error -i "$OUT" -f f32le - | python3 -c "import sys,numpy as np; a=np.abs(np.frombuffer(sys.stdin.buffer.read(),np.float32)); print('| max', round(float(a.max()),3), 'n>0.9', int((a>0.9).sum()))"
