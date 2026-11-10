# Explainer #3 working pack (Amplify 24x made simple, the market stall), 9 Nov 2026

Every voice line explainer #3 uses, already cut, as lossless FLAC (`v_<key>.flac`), with `lines.json` (source and cut
points) and `words.json` (word times). Decode each to `v_<key>.wav` (48 kHz mono) next to the files in
`tools/jetup-explainers/ex3/` (working branch, later main) and `make_ex3.py` runs without re-cutting anything:

    for f in v_*.flac; do ffmpeg -v error -y -i "$f" -ar 48000 -ac 1 "${f%.flac}.wav"; done

The first preview (2:01, 9 Nov 2026) uses these banked lines only: 0 credits.

## The six new lines: recorded 10 Nov 2026 in MTG Master Voice V3

MTG approved the lines, then chose **MTG Master Voice V3** (`65f1b9ff3f1e418496de5715a801e7dd`) as his voice from now on
("V3 sounds better, sounds exactly like me"). One request with explainer #4's two lines, 1 credit (51 left), banked as
`../ex3ex4v3.flac` with its text (`../ex3ex4v3.txt`) and HeyGen's reply with word times (`../ex3ex4v3_tts.json`).
Cut on the pauses, levelled to -18.5 LUFS like the recorded lines around them, checked word for word with faster-whisper:
`v_nhook.flac`, `v_nstall.flac`, `v_nmove.flac`, `v_nlimit.flac`, `v_ncalc.flac`, `v_nrecap.flac`. `lines.json` and
`words.json` here now hold all 35 lines, so `make_ex3.py` builds the version with the spoken hook, stall, move, loss limit,
calculator and recap (2:13).
