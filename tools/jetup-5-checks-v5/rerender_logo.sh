#!/bin/bash
# 5 Checks v5.3 (MTG, 8 Nov 2026): the JetUP logo disc in place of every photo of MTG (cards, slogan, signature, end card,
# top-left badge). Same timeline and the same approved v5.1 audio (mix_v5.wav). The avatar stays as approved.
set -e
cd "$(dirname "$0")"
DISC=/home/user/mtgtribe/tools/jetup-tutorial/jetup-disc.png
N=$(python3 -c "import json;print(len(json.load(open('tl.json'))['frames']))")
Q=$(( (N + 3) / 4 )); rm -f parts/status.txt
for i in 0 1 2 3; do a=$((i*Q)); b=$(( (i+1)*Q < N ? (i+1)*Q : N ));
  (PHOTO=$DISC FACE=$DISC python3 render.py range $a $b parts/p$i.mp4 > parts/log$i.txt 2>&1; echo "done $i $?" >> parts/status.txt) & done; wait
cat parts/status.txt
ffmpeg -v error -y -f concat -safe 0 -i parts/list.txt -c copy v5_video.mp4
ffmpeg -v error -y -i v5_video.mp4 -i mix_v5.wav -map 0:v -map 1:a -c:v copy -af apad -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart ../out/JetUP_5_Checks_MTG_v5.3.mp4
cd ../out && ffmpeg -v error -y -i JetUP_5_Checks_MTG_v5.3.mp4 -c:v libx264 -preset slow -crf 22 -tune film -pix_fmt yuv420p -g 50 -c:a copy -movflags +faststart JetUP_5_Checks_MTG_v5.3_web.mp4
ffmpeg -v error -y -ss 0.5 -i JetUP_5_Checks_MTG_v5.3.mp4 -frames:v 1 -vf scale=1280:720 -q:v 2 JetUP_5_Checks_MTG_v5.3_thumbnail.jpg
ls -la JetUP_5_Checks_MTG_v5.3*; ffprobe -v error -show_entries format=duration -of csv=p=0 JetUP_5_Checks_MTG_v5.3_web.mp4
