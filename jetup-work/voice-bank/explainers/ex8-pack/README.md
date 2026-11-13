# Explainer #8 working pack (getting your money out: the fruit tree), 12 Nov 2026

MTG approved ten new lines on 12 Nov 2026 ("Yes, record (1 credit)"). One request in **MTG Master Voice V3**
(`65f1b9ff3f1e418496de5715a801e7dd`), no model or engine override, one paragraph per line, 1 credit (48 before, 47 after,
resets 3 Dec 2026). The whole take is `../ex8v3.flac` with its text (`../ex8v3.txt`) and HeyGen's reply with word times
and the cut points (`../ex8v3_tts.json`).

The ten new lines, cut with their edges snapped to the silence and levelled to -18.5 LUFS like MTG's other V3 lines:
`v_nhook`, `v_ntree`, `v_nyard`, `v_nmoney`, `v_nfruit`, `v_nbranch`, `v_nbasket`, `v_nroute`, `v_n48`, `v_nrecap`.
HeyGen's word times for nbranch, nbasket, nroute, n48 and nrecap ran 0.17 to 0.19 s ahead of the audio; `words.json`
here already has them shifted.

Six recorded lines newly cut for explainer #8 (0 credits): `v_advice` ("My advice?"), `v_word` ("Don't take my word for
it.") and `v_login` ("Log in yourself, and see your own balance.") from the 5 Checks takes on their forced-alignment word
times, and `v_bonus`, `v_ends`, `v_change` (the promo rules) from `signup-training/t3.mp3` at explainer #5's cuts.

Every line was checked with faster-whisper: all sixteen read as written ("TAG" as the word tag, "Jet Up's" as two words).
`lines.json` and `words.json` hold the cut points and word times. Decode each to `v_<key>.wav` (48 kHz mono) next to
`tools/jetup-explainers/ex8/`:

    for f in v_*.flac; do ffmpeg -v error -y -i "$f" -ar 48000 -ac 1 "${f%.flac}.wav"; done

The greeting, "Profits can be withdrawn any time.", "Start small...", "Let the system prove itself to you.", the close,
the fair-play lines and the signature ending come from `../ex4-pack/`. Live on mtgtribe.com/jetup since 12 Nov 2026
(How it works "Withdrawals", the 5 Checks page check 5, the Videos page). Facts: `tools/learning-system/jetup-facts.md`.
