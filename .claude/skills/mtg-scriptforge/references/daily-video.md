# Today's video (MTG: "let's create today's video")

MTG, 7 November 2026: "All I want to say every day is something like 'let's create today's video', then you do the
rest, cycling through those hooks and more, making sure each video is unique, educational, punchy." When he says that
(or anything like it), run this whole routine without asking what to make.

## 1. Read the log

`tools/videos/README.md` lists every video: number, hook format, topic, length, status. Today's video gets the next
number and a new folder `tools/videos/<nn>-<slug>/`.

## 2. Pick the hook format (rotate, never the same format two days running)

1. Did You Know ...?
2. What If ...?
3. What Everyone Ought to Know About ...
4. The Truth About ... / Myth or Fact?
5. How ... Really Works
6. The Hidden Cost of ...
7. Before You ... (a short safety checklist)
8. The Story of ... (money history)
9. Can You Guess ...? (a quiz with the answer at the end)
10. Why Most People ... (money psychology)

Then start again at 1. Change the opening line itself every time, never a copy of an earlier hook.

## 3. Pick a fresh topic from MTG's niche

Topic families (rotate them too): money history, how money and banks really work, crypto and blockchain basics,
scam awareness and staying safe, everyday money psychology, digital tools and skills, bridge topics from the niche menu
(self-improvement, psychology, science, history). Never repeat a topic and angle already in the log. Prefer topics where
research shows big interest and a gap (strong long videos, weak or no Shorts).

## 4. Length and layout

Default: a Short, 45 to 60 seconds, 9:16 (MTG posts vertical first). About once a week, a long video (3 to 5 minutes)
when the topic deserves it, plus 2 or 3 Shorts cut from it. Shorts skip the greeting (hook, one idea, one prompt, one
call to action, short sign-off). Long videos greet with the right type word ("this video", "this tutorial", ...).

## 5. Make it (same rules as every video)

1. Research brief (`scripts/yt_research.py`, at least five comparable videos with real numbers, the gap, "better than"
   points, verified facts with sources).
2. Script in MTG's voice, compliance scan (`scripts/compliance_scan.py`) and human check.
3. Voice: reuse the voice bank first. Otherwise one HeyGen speech call for the finished script, in "MTG Master Voice V2"
   only. Credits follow MTG's standing approval below; anything above it (or any Leo clip) waits for his yes.
4. Leo: reuse his existing clips first (video 01: V2 asks a question, V3 amazed, V5 thinking, V6 laughs in disbelief,
   V7 makes a point, L2 open paw); new clips only with MTG's go-ahead.
5. Build in the house format (video 01 as posted): gold-and-black 2.5D scenes, 3D card entrances, slow push-in, Leo in
   gold windows, word-by-word captions, soft effects fitted to this story, MTG's theme from 50 s before the end, the
   mtgtribe.com card, a designed cover.
6. QC frames, render, loudness -14 LUFS, checks, cover embedded, posting pack (`references/posting-pack.md`).
7. Send MTG the preview, the cover and the posting texts. He posts it himself. Never publish.
8. Add the video to the log.

## Standing approval for credits

**Approved by MTG on 7 November 2026:** up to 5 HeyGen credits per daily video for the voice recording, without
asking. New Leo clips (about 15 credits each) and anything above 5 credits still need his yes. Check the balance with
`get_current_user` first; if a generation fails, ask before trying again.
