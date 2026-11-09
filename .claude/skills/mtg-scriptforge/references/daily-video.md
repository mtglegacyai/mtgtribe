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

## MTG's direction (9 November 2026): mix it up, grow the tribe, then sell

MTG: "Talk more about Bitcoin, about crypto, about blockchain, about AI, about side hustles, and just mix it all
together ... giving tips ... without any guarantees ... speak to people who are looking for ways to make money online
... we are also growing the tribe ... I want to grow my tribe. And then I want to sell ... that order is important ...
take it up a notch ... be more compelling."

- **Who we talk to:** one person who wants to make money online, is curious about Bitcoin and crypto and wants
  multiple streams of income, but is busy, a bit confused and wary of scams. Speak to that person ("you").
- **Topic mix (rotate, never the same family two days running):** Bitcoin; crypto and blockchain; AI tools and AI
  skills; side hustles and making money online (honest tips); multiple streams of income; scam awareness; money and
  banks (at most one video in four).
- **The order: tribe first, then sell.** Every Short gives value, then invites people into the free MTG TRIBE. Selling
  happens later, in the tribe and on MTG's websites (dashboards, opportunity guides), never as a pitch in a social
  video (`compliance.md`).
- **Take it up a notch (every script passes all seven):**
  1. The first second speaks to one person and names their problem or wish ("If Bitcoin still confuses you...").
  2. A big, true, specific number or a surprise in the first 3 seconds.
  3. An open loop that pays off later ("number three is where people lose everything").
  4. Fast beats: numbered steps, short punchy sentences, a new visual every 2 to 3 seconds.
  5. One practical tip they can use today, with no guarantees.
  6. A question that invites real answers and feeds the next videos ("Ask me below, I'll answer in my next videos").
  7. The tribe invite with a reason (what they get inside), then the website.
- **CTAs:** spoken: "Join the free MTG TRIBE at MTG tribe dot com slash group". On screen: mtgtribe.com/group (join
  the tribe) and mtgtribe.com (tutorials, explainers, honest guides, risks included). mtgtribe.com/group is a page on
  MTG's own website that forwards to the WhatsApp group: if WhatsApp ever closes a group, MTG points /group somewhere
  new and every video still works. Never show or say the raw chat.whatsapp.com link.
- **What the tribe is (as mtgtribe.com describes it):** a WhatsApp community of action takers: tutorials, explainers,
  tips and strategies across different opportunities, crypto, AI skills and multiple streams of income, learning
  together. Never promise anything the tribe does not do.
- **The plan of the next videos** lives in `tools/videos/PLAN.md`; follow it unless research or MTG says otherwise.

## 3. Pick a fresh topic from MTG's niche

Topic families: see MTG's direction above (Bitcoin, crypto and blockchain, AI, side hustles and making money online,
multiple streams of income, scam awareness, money at most one video in four), plus bridge topics from the niche menu
(self-improvement, psychology, science, history) now and then. Never repeat a topic and angle already in the log.
Prefer topics where research shows big interest and a gap (strong long videos, weak or no Shorts).

## 4. Length and layout

Always a vertical Short (9:16) of **at most 60 seconds, never longer** (MTG, 7 November 2026: "I like the short
videos more, up to 1 minute, and not longer"). About 130 to 145 spoken words for 50 to 55 seconds, plus about 3 seconds
for the theme's last line at the end. Shorts skip the greeting: hook, one idea in 3 or 4 beats, one prompt, one call to
action, short sign-off ("I'm MTG, Your Digital Architect. Let's Get This Crypto!").

## 5. Make it (same rules as every video)

1. Research brief (`scripts/yt_research.py`, at least five comparable videos with real numbers, the gap, "better than"
   points, verified facts with sources).
2. Script in MTG's voice, compliance scan (`scripts/compliance_scan.py`) and human check.
3. Voice: reuse the voice bank first. Otherwise one HeyGen speech call for the finished script, in "MTG Master Voice V2"
   only. Credits follow MTG's standing approval below; anything above it (or any Leo clip) waits for his yes.
4. Leo: reuse his existing clips first (video 01: V2 asks a question, V3 amazed, V5 thinking, V6 laughs in disbelief,
   V7 makes a point, L2 open paw); new clips only with MTG's go-ahead.
5. Build in the house format (video 01 as posted): gold-and-black 2.5D scenes, 3D card entrances, slow push-in, Leo in
   gold windows, word-by-word captions, soft effects fitted to this story, only the last line of his theme ("Let's get
   this crypto, wherever I go!") right after his last word, the tribe and website card (mtgtribe.com/group and
   mtgtribe.com), his formal photo in the gold circle (since 9 November 2026), a designed cover.
6. QC frames, render, loudness -14 LUFS, checks, cover embedded, posting pack (`references/posting-pack.md`).
7. Send MTG the preview, the cover and the posting texts. He posts it himself. Never publish.
8. Add the video to the log.

## Standing approval for credits

**Approved by MTG on 7 November 2026:** up to 5 HeyGen credits per daily video for the voice recording, without
asking. New Leo clips (about 15 credits each) and anything above 5 credits still need his yes. Check the balance with
`get_current_user` first; if a generation fails, ask before trying again.
