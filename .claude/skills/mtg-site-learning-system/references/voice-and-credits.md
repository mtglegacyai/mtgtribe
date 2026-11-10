# Voice and credits

## The facts to state plainly

- MTG's only approved voice is HeyGen **MTG Master Voice V3** (voice ID `65f1b9ff3f1e418496de5715a801e7dd`), his voice since 10 Nov 2026
  ("V3 sounds better, sounds exactly like me"). Call it with no model and no engine override, and no break tags (one
  paragraph per pause). The older V2 (`3931c505632149ceb2bbfecf2778c09c`) is retired because HeyGen's new voice model
  refuses it; its banked recordings stay usable. Never another voice, never ElevenLabs, never a stand-in.
- Measured on V3 (10 Nov 2026): 1 credit for 51 seconds of speech (about 900 characters).
- There is no stored copy of his voice that can say new words. What exists is a **voice bank**: the real recordings he
  has already approved, with word timings. Any sentence in the bank can be reused for free. Any new sentence needs a new
  HeyGen speech request, which costs credits, so it needs MTG's approval first.
- Cost: measured at 14 credits for 5,400 characters of speech (about 1.3 credits per 500 characters); budget **about
  2 credits per 500 characters** to be safe. One minute of narration is roughly 150 words or 900 characters, so about
  3 to 4 credits. A full avatar render is far more expensive
  (about 48 credits per minute), so explainers are motion graphics in his voice, not avatar renders, unless he asks.
- After any HeyGen task, report the credits remaining (MTG does not like surprises).

## Voice banks

- **JetUP and TAG Markets:** repository `mtglegacyai/mtgtribe`, branch `jetup-video-work`, folder `jetup-work/voice-bank/`
  (5 Checks and sign-up training narration, about 15 minutes, 262 sentences, `sentences.tsv` index, README).
- Every other site: create `<site>-video-work/voice-bank/` on that site's working branch the first time a speech
  request is made for it, with the same layout (original files exactly as HeyGen delivered them, the HeyGen response
  JSON with `word_timestamps`, the script text that was sent, and a `sentences.tsv` index). A line approved for one site
  can be reused on another only if the words are still true there.

## Building a script from the bank

1. Write the ideal script for the video first (hook, picture, numbers, where the picture stops, call to action).
2. Search `sentences.tsv` for each idea. Use a recorded sentence when it says the same thing truthfully, even if the
   wording differs a little from your ideal; MTG's approved wording beats yours.
3. Mark what is left as **new lines**, keep them short, and estimate their credits.
4. Show MTG the script with each line tagged "recorded" or "new", plus the credit total. He may approve the new lines,
   ask for on-screen text instead, or change the script.

Cutting and joining: leave about 0.05 s before the first word and 0.15 s after the last, cut on natural pauses, add
2 to 5 ms fades at the joins, keep one steady pace (even out phrases gently, never stretch the voice beyond about
0.94x to 1.10x), and loudness-normalise the final mix. Lines from different recordings of the same voice and engine join
well; listen to every join.

## Making new lines (only after approval)

- Use HeyGen's speech tool with MTG's voice ID and no engine, settings or language override, then confirm the response
  says `"engine": "orca"`. One request for all of a video's new lines (joined with short breaks) is cheaper and keeps
  the delivery consistent.
- Download the audio immediately (links expire), add it to the site's voice bank with its JSON and script, re-index
  `sentences.tsv`, and commit it to the working branch.
- Spell numbers and abbreviations the way they should be spoken ("X A U, U S D", "twenty-four times").
