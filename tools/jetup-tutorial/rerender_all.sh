#!/bin/bash
# Re-render tutorial parts 1 to 3 with the JetUP logo disc (no MTG photo), keep the approved audio mixes.
set -e
for spec in "p1:JetUP_Tutorial_Part1_Create_Account_v4_9x16.mp4" "p2b:JetUP_Tutorial_Part2_Link_TAG_Markets_v2_9x16.mp4" "p3b:JetUP_Tutorial_Part3_Verify_Identity_v2_9x16.mp4"; do
  d=${spec%%:*}; out=${spec#*:}
  cd /tmp/claude-0/-home-user-mtgtribe/a6cc0db9-d96c-55e0-8645-be8a10935550/scratchpad/tutorial/$d
  N=$(node -e "global.window={};eval(require('fs').readFileSync('stage/timeline.js','utf8'));console.log(Math.round(window.TL.T*window.TL.fps))")
  Q=$(( (N + 3) / 4 ))
  rm -rf frames && mkdir frames
  node render.js range 0 $Q frames > r0.log 2>&1 &
  node render.js range $Q $((2*Q)) frames > r1.log 2>&1 &
  node render.js range $((2*Q)) $((3*Q)) frames > r2.log 2>&1 &
  node render.js range $((3*Q)) $N frames > r3.log 2>&1 &
  wait
  echo "$d rendered $(ls frames | wc -l) of $N"
  ffmpeg -v error -y -framerate 30 -i frames/f%05d.jpg -i mix.wav -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest $out
  echo "$d encoded $out $(ffprobe -v error -show_entries format=duration -of csv=p=0 $out)"
done
echo ALLDONE
