#!/bin/bash
# Extracts the banked takes this video uses from MTG's voice bank (branch jetup-video-work) into bank/.
set -e; cd "$(dirname "$(readlink -f "$0")")"; mkdir -p bank; V=origin/jetup-video-work:jetup-work/voice-bank
git fetch -q origin jetup-video-work
git show $V/signup-training/t1.mp3 > bank/t1.mp3; git show $V/tutorial/p1v2.mp3 > bank/p1v2.mp3
git show $V/explainers/ex4-pack/words.json > bank/ex4_words.json
for k in n_turn2 every n_save n_share n_we n_slog o_fin o_dyor o_thanks o_support o_massive o_best o_im o_see o_lgtc; do
  git show $V/explainers/ex4-pack/v_$k.flac > bank/v_$k.flac; ffmpeg -v error -y -i bank/v_$k.flac -ar 48000 -ac 1 bank/v_$k.wav; rm bank/v_$k.flac
done
echo "bank ready: $(ls bank | wc -l) files"
