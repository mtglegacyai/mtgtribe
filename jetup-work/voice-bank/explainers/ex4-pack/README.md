# Explainer #4 working pack (the 70/30 split), 9 Nov 2026

Every voice line explainer #4 uses, already cut, as lossless FLAC (`v_<key>.flac`), with `lines.json` (source and cut
points) and `words.json` (word times). Decode each to `v_<key>.wav` (48 kHz mono) next to the files in
`tools/jetup-explainers/ex4/` (main branch) and `make_ex4.py` runs without re-cutting anything:

    for f in v_*.flac; do ffmpeg -v error -y -i "$f" -ar 48000 -ac 1 "${f%.flac}.wav"; done

Still to add (MTG approved about 1 credit on 9 Nov 2026; HeyGen's connection had expired in that session):
one create_speech call, voice "MTG Master Voice V2" (3931c505632149ceb2bbfecf2778c09c), no engine parameter:

    Seventy, thirty. Two numbers that decide where every profit goes. Let me show you. <break time="0.8s"/> Want to try it
    with your own numbers? Open the Profit Split Calculator on my page, type an amount and a result, and see your share in one tap.

Save it here as `../ex4v1.mp3` (+ `_tagged.txt`, `_tts.json`), cut it at the 0.8 s break into `v_nhook.wav` and
`v_ncalc.wav`, add both to `lines.json` (keys `nhook`, `ncalc`) and their word times to `words.json` (the `words_for`
helper in `lines_ex4.py`), then run `make_ex4.py`: it switches to the new hook and the spoken calculator line by itself.
Font: `jetup-work/engine/fonts/Anton-Regular.ttf`. JetUP disc and logo: `tools/jetup-tutorial/` and `jetup/img/` on main.

**10 Nov 2026: still not recorded.** HeyGen now refuses MTG Master Voice V2 through its connector ("This voice is not
compatible with heygen-voice-1. Create a new instant voice."). See `../ex3-pack/README.md` and
`tools/learning-system/PLAN.md`, "Voice". Do not retry or substitute until MTG has decided. Break tags are not supported
for instant voices on the new model: send the two lines as two plain paragraphs.

**Recorded 10 Nov 2026 in MTG Master Voice V3** (MTG's voice from now on): `v_nhook.flac` and `v_ncalc.flac`, from the
same request as explainer #3's six lines (`../ex3ex4v3.flac`, 1 credit). `lines.json` and `words.json` here include them,
so `make_ex4.py` builds the version with the spoken hook and calculator line (2:16).
