# Explainer #3 working pack (Amplify 24x made simple, the market stall), 9 Nov 2026

Every voice line explainer #3 uses, already cut, as lossless FLAC (`v_<key>.flac`), with `lines.json` (source and cut
points) and `words.json` (word times). Decode each to `v_<key>.wav` (48 kHz mono) next to the files in
`tools/jetup-explainers/ex3/` (working branch, later main) and `make_ex3.py` runs without re-cutting anything:

    for f in v_*.flac; do ffmpeg -v error -y -i "$f" -ar 48000 -ac 1 "${f%.flac}.wav"; done

The first preview (2:01, 9 Nov 2026) uses these banked lines only: 0 credits.

## Still to add: six new lines (NOT approved yet, ask MTG first, about 3 credits)

HeyGen's speech access returned "Bearer token expired/revoked" in the session that built the preview, so nothing was
recorded and nothing was charged. Once MTG has approved the lines and reconnected HeyGen (new session): check the credit
balance, then one create_speech call, voice "MTG Master Voice V2" (3931c505632149ceb2bbfecf2778c09c), no engine
parameter (the reply must say engine "orca"), with word timestamps:

    Fifty dollars that trades like twelve hundred. How? One word: Amplify. Let me show you. <break time="0.8s"/> Think of a
    market stall. You pay for one stall, but Amplify lets you trade as if you had twenty-four. <break time="0.8s"/> Same
    market, same prices. Every move is twenty-four times bigger, in both directions. <break time="0.8s"/> And the loss limit
    is written down before you start: ten percent of the starting balance, or five percent with a community token.
    <break time="0.8s"/> Want to try it with your own numbers? Open the Exposure Calculator on my page, type an amount, and
    see your trading size in one tap. <break time="0.8s"/> So that's Amplify: a bigger trading size, not extra money. Start
    small, and learn how it moves.

Never retry by yourself after an error or a timeout: ask MTG first. Report the credits left afterwards.

Save it here as `../ex3v1.mp3` (+ `_tagged.txt`, `_tts.json`), cut it at the 0.8 s breaks into `v_nhook.wav`,
`v_nstall.wav`, `v_nmove.wav`, `v_nlimit.wav`, `v_ncalc.wav` and `v_nrecap.wav`, add them to `lines.json` (keys `nhook`,
`nstall`, `nmove`, `nlimit`, `ncalc`, `nrecap`) and their word times to `words.json` (the `words_for` helper in
`lines_ex3.py`), re-index `../../sentences.tsv`, then run `make_ex3.py`: it switches to the spoken hook, stall, move,
loss limit, calculator and recap by itself. Listen to every new line before building (numbers, "Amplify", "twenty-four").
Font: `jetup-work/engine/fonts/Anton-Regular.ttf`. JetUP disc and logo: `tools/jetup-tutorial/` and `jetup/img/` on main.
