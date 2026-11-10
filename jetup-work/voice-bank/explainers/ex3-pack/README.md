# Explainer #3 working pack (Amplify 24x made simple, the market stall), 9 Nov 2026

Every voice line explainer #3 uses, already cut, as lossless FLAC (`v_<key>.flac`), with `lines.json` (source and cut
points) and `words.json` (word times). Decode each to `v_<key>.wav` (48 kHz mono) next to the files in
`tools/jetup-explainers/ex3/` (working branch, later main) and `make_ex3.py` runs without re-cutting anything:

    for f in v_*.flac; do ffmpeg -v error -y -i "$f" -ar 48000 -ac 1 "${f%.flac}.wav"; done

The first preview (2:01, 9 Nov 2026) uses these banked lines only: 0 credits.

## Still to add: six new lines (approved by MTG on 10 Nov 2026, about 3 credits, NOT recorded yet)

**Blocked on 10 Nov 2026: read this before any speech request.** HeyGen was connected again (54 credits), and one
request was sent with voice "MTG Master Voice V2" (3931c505632149ceb2bbfecf2778c09c), no model, no settings, word
timestamps on. HeyGen refused it: "This voice is not compatible with heygen-voice-1. Create a new instant voice." (400,
not retryable, nothing charged: 54 credits before and after). HeyGen's connector now speaks with its new model, and its
documentation says instant voices made before it "must be cloned again before they can speak here" (closest match:
similarity "max", expressiveness 0.5). Break tags are not supported for instant voices there either: send plain
paragraphs and cut on the pauses with the word times.

Do not retry, do not pass a model, do not use another voice, do not clone anything until MTG has decided how his voice
is produced (his options are in `tools/learning-system/PLAN.md`, "Voice", on the working branch and main).

The exact text, one paragraph per line:

    Fifty dollars that trades like twelve hundred. How? One word: Amplify. Let me show you.

    Think of a market stall. You pay for one stall, but Amplify lets you trade as if you had twenty-four.

    Same market, same prices. Every move is twenty-four times bigger, in both directions.

    And the loss limit is written down before you start: ten percent of the starting balance, or five percent with a
    community token.

    Want to try it with your own numbers? Open the Exposure Calculator on my page, type an amount, and see your trading
    size in one tap.

    So that's Amplify: a bigger trading size, not extra money. Start small, and learn how it moves.

When the audio exists (from HeyGen or as a file MTG sends): save it here as `../ex3v1.mp3` (+ the exact text and the
reply or a note of where it came from), cut it into `v_nhook.wav`, `v_nstall.wav`, `v_nmove.wav`, `v_nlimit.wav`,
`v_ncalc.wav` and `v_nrecap.wav`, add them to `lines.json` (keys `nhook`, `nstall`, `nmove`, `nlimit`, `ncalc`,
`nrecap`) and their word times to `words.json` (the `words_for` helper in `lines_ex3.py`), re-index
`../../sentences.tsv`, then run `make_ex3.py`: it switches to the spoken hook, stall, move, loss limit, calculator and
recap by itself. Listen to every new line before building (numbers, "Amplify", "twenty-four"), and compare its sound
with the banked lines beside it. Report the credits left.
Font: `jetup-work/engine/fonts/Anton-Regular.ttf`. JetUP disc and logo: `tools/jetup-tutorial/` and `jetup/img/` on main.
