#!/bin/bash
# Re-mux a finished video's audio at AAC 256k (the native encoder at 192k put a 5-sample overshoot into Part 2), keep the
# picture, then check: loudness, true peak and no decoded sample above 0.9.
set -e
V=$1; M=$2; T=$(mktemp --suffix=.mp4 -p "$(dirname "$V")")
ffmpeg -v error -y -i "$V" -i "$M" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest "$T" && mv "$T" "$V"
ffmpeg -v info -nostats -i "$V" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2 | tr -s ' ' | tr '\n' ' '
ffmpeg -v error -i "$V" -f f32le - | python3 -c "import sys,numpy as np; a=np.abs(np.frombuffer(sys.stdin.buffer.read(),np.float32)); print('| max', round(float(a.max()),3), 'n>0.9', int((a>0.9).sum()))"
