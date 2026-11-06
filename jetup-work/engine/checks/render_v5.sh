#!/bin/bash
# v3 final: native 25 fps, single HeyGen take, avatar shifted right with blurred fill + frosted panel, overlay, voice + closing track.
set -e
cd /home/claude/jv
OUT=${1:-JetUP_5_Checks_MTG_v4_video.mp4}
read SE TOT <<< $(python3 -c "import json;t=json.load(open('timeline5.json'));print(t['speech_end'],t['total'])")
MS=$(python3 -c "print(max(0, $TOT - 51.36))")          # closing track starts 50+ s before the end
SL=$(python3 -c "print($SE - $MS)")                      # where speech ends inside the track
MSMS=$(python3 -c "print(int($MS*1000))")
VG=${VG:-12.6}                                            # voice gain in dB before the mix (-32.6 LUFS wav -> -20)
OFFS=${OFFS:-100}                                         # ms the HeyGen lips run ahead of the voice: voice starts this much earlier
VD=$(python3 -c "print(int(1000 - $OFFS))")
COVER=1.0; END=5.0
[ ov5.mov -nt seq5.txt ] || ffmpeg -v error -y -f concat -safe 0 -i seq5.txt -vf "fps=25,format=rgba" -c:v png -pix_fmt rgba ov5.mov
ffmpeg -v error -y -i ov5.mov -i v3/av.mp4 -filter_complex "
[1:v]fps=25,scale=1920:1080,setsar=1,tpad=start_duration=${COVER}:start_mode=clone:stop_duration=${END}:stop_mode=clone,split=2[src][src2];
[src]scale=480:270,boxblur=10:2,scale=1920:1080,eq=brightness=-0.12:saturation=0.8[bg];
[src2]crop=1590:1080:0:0[fg];
[bg][fg]overlay=330:0,split=2[st][st2];
[st2]crop=764:830:48:118,scale=191:208,boxblur=6:2,scale=764:830[gl];
[st][gl]overlay=48:118[base];
[base][0:v]overlay=0:0:shortest=1,format=yuv420p[v]
" -map "[v]" -t ${TOT} -c:v libx264 -preset veryfast -crf 19 -r 25 -an -movflags +faststart $OUT
ffprobe -v error -show_entries format=duration:stream=width,height,codec_name,r_frame_rate -of compact $OUT
