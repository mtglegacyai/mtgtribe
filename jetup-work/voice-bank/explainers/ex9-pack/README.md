# Explainer #9 working pack (what copying really means: the cooking class), 13 Nov 2026

MTG approved eight new lines on 13 Nov 2026 ("Yes, record (1 credit)"). One request in **MTG Master Voice V3**
(`65f1b9ff3f1e418496de5715a801e7dd`), no model or engine override, one paragraph per line, 1 credit (44 before, 43 after,
resets 3 Dec 2026). The whole take is `../ex9v3.flac` with its text (`../ex9v3.txt`) and HeyGen's reply with word times
and the cut points (`../ex9v3_tts.json`).

The eight new lines, cut with their edges snapped to the silence and levelled to -18.5 LUFS like MTG's other V3 lines:
`v_nhook`, `v_ncook`, `v_ntwist`, `v_npot`, `v_nauto`, `v_nyours`, `v_nlid`, `v_nrecap`. HeyGen's word times for nauto,
nyours, nlid and nrecap ran 0.19 to 0.21 s ahead of the audio; `words.json` here already has them shifted. Useful on
their own: "You don't pick the trades.", "You pick the strategy, how much to put in, and when to stop." (the How it works
page's own sentence), "With your investor password, you can watch every trade, read-only." (said "reed only", measured).

Four recorded lines newly cut for explainer #9 (0 credits): `v_deposit` ("Your deposit goes into an M T five account at
TAG Markets, in your name.") and `v_copyx` ("Then you connect a strategy through CopyX.") from the 5 Checks take o1 on
its forced-alignment word times, and `v_terms` ("Read the terms.") and `v_perf` ("A thirty percent performance fee, taken
from profits only.") from `signup-training/t3.mp3`: one stretch split in its own silence, so play `v_perf` straight after
`v_terms` with no gap.

Every line was checked with faster-whisper ("Your pot" reads as "Your part" when cut on its own and as "pot" after the
cooking class line). `lines.json` and `words.json` hold the cut points and word times. Decode each to `v_<key>.wav`
(48 kHz mono) next to `tools/jetup-explainers/ex9/`:

    for f in v_*.flac; do ffmpeg -v error -y -i "$f" -ar 48000 -ac 1 "${f%.flac}.wav"; done

The Myfxbook line, the greeting, the close, the fair-play lines and the signature ending come from `../ex4-pack/`.
Facts: `tools/learning-system/jetup-facts.md`.
