# Explainer #6 working pack (the partner plan: the rule most people miss), 11 Nov 2026

MTG approved nine new lines on 11 Nov 2026 ("Approved"). One request in **MTG Master Voice V3**
(`65f1b9ff3f1e418496de5715a801e7dd`), no model or engine override, one paragraph per pause, 1 credit (49 left, resets
3 Dec 2026). The whole take is `../ex6v3.flac` with its text (`../ex6v3.txt`) and HeyGen's reply with word times
(`../ex6v3_tts.json`).

Cut on the pauses, levelled to -18.5 LUFS like MTG's other V3 lines, and checked word for word with faster-whisper
(all nine match; "deposits" at the end of `nlots` was confirmed by its final "s"): `v_nhook`, `v_nlevel`, `v_nfloors`,
`v_nqual`, `v_nfourth`, `v_nlots`, `v_nshare`, `v_nclient`, `v_nrecap` (FLAC). `lines.json` and `words.json` hold the
cut points and word times. Decode each to `v_<key>.wav` (48 kHz mono) next to `tools/jetup-explainers/ex6/`:

    for f in v_*.flac; do ffmpeg -v error -y -i "$f" -ar 48000 -ac 1 "${f%.flac}.wav"; done

The greeting, close and signature lines come from explainers #1 and #2 (see `../ex3-pack/`).
Facts: `tools/learning-system/jetup-facts.md` (partner plan, how levels open), JetUP's business plan, Oct 2026.
