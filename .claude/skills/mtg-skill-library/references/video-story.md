# Video story: hooks, reels, explainers and video ads that hold attention

Use for tutorials, explainers, promos, reels, shorts, video ads and VSLs, together with MTG's video skills
(mtg-tutorial-video, mtg-promo-video, mtg-scriptforge). His rules stay on top: V3 voice only, the signature ending and
end card, the closing track rule, privacy in every frame, captions synced to the final audio, one focal point at a time.

Sources: Herk Edit Kit by Nate Herk (MIT, `nateherkai/herk-edit-kit` at 10511e5af86f: the video-storytelling and
short-form-edit skills and the editing playbook, measured on his 27 top reels) and HyperFrames by HeyGen (Apache 2.0,
`heygen-com/hyperframes` at cb9dfa8f0c9e). Adapted for MTG.

## The first three seconds are their own edit

Plan them separately, on paper, before building anything:

- **What the viewer gains**, the **question left open**, the **evidence on screen by second three**, and **the scene
  where the payoff comes**. Reject vague teasing and any promise the video can't keep.
- **The first frame means something on its own** (it is also the preview, as mtg-promo-video already asks): a surprising
  result, a contradiction, a glimpse of the outcome, a real expression.
- **It works muted.** The topic or tension is readable without sound, and a second meaningful change happens before
  second three.
- No logo bumper, no added silence, no flash for its own sake, no "STOP" stamped on every video. Vary the device.
- Sound: the hit lands within two frames of the picture, and the first spoken word still comes through clearly.
- Check the encoded opening frame by frame before the preview.

## The short-form reel formula

The source video MTG sent on 25 Nov 2026 follows this exactly, and it is the shape of many winning "list" reels:

1. Hook in the first three seconds that names the topic or tool.
2. One line of credibility or context.
3. If it is a list, **show every item early, blurred or small, as an open loop** (the viewer wants to see them all).
4. Each item: its own title card, a one-line definition, two or three literal visuals, emphasis on the key line.
5. A resolution that calls back to the hook.
6. Call to action: **show the reward first** (the guide, the page), then the action (the link, or "comment GUIDE").

Pacing measured on Nate's top reels, as a starting point and not a law: speech starts at once, pauses between phrases
under about 0.2 s, shots of about 1.1 to 1.4 s (none over about 2.8 s), the first cut on the first charged word, each
spoken list item gets its own shot.

**For MTG:** his reels keep his signature ending and end card (Nate uses no outro card; MTG's 8 Nov 2026 rule wins), and
videos of 60 s or less take only the last line of the closing track. A "comment a word to get the guide" call to action
passes mtg-scriptforge's compliance gate first, and the reward must be real (his PDF guide, a page).

## Every vertical video, whatever tool builds it (from HyperFrames' checker, 26 Nov 2026)

- **Words inside the apps' safe area.** On 1080 x 1920, TikTok, Reels and Shorts all leave clear from 288 to 1248 px
  down and 120 to 888 px across, narrowing to 780 px on the right below 840 px down (TikTok's button rail). Outside it
  only background and decoration. Burned-in captions sit at the bottom of that band.
- **Nothing a viewer must read under 28 px**, and about 5 words per line for a claim: cut words, never shrink them.
- **Closing lines stay long enough to read:** at least 0.5 s plus 0.3 s per word, and at least 2 s before the video
  ends. This applies to the address, the call to action and MTG's signature line.
- Frame 0 is the thumbnail and the hook: never black, never a logo alone.

## Explainers: one world the camera moves through

- **One persistent world.** The video lives in one space that never resets. What has been drawn stays where it was; new
  things are added, not swapped in. Decide what directions mean (for example, left to right is toward the result) and
  keep that for the whole video; break it once, on purpose, for meaning.
- **The camera is the edit.** Cutting to a new graphic costs the viewer their bearings; moving through a space that stays
  put costs nothing. Three distances: the whole world (orient, payoff), a region (most of the time), one detail (a
  number, a decision). Pulling back at the end pays off everything built so far.
- **Attention is a spotlight.** Exactly one thing at full brightness at a time; what was drawn before stays quiet but
  readable; what has finished its job leaves. This is MTG's "one focal point at a time", made precise.
- **If it doesn't get a word, it doesn't get drawn.** Every visual is tied to a spoken line.
- **Open loops are spatial.** Never say "we'll come back to this"; leave something visibly unfinished and return to it.

Craft rules that each cost a rebuild to learn:

- No label within 60 px of the frame edge; a word cut mid-letter reads as a bug.
- Two moves in a row on the same subject read as a glitch. Merge them into one smooth gesture.
- A camera move and a full-screen wipe happen one after the other, never together.
- Reuse the exact same framing for the same purpose; near-identical framings look like drift.
- Move time grows with the distance travelled; no single preset for every move.

## Tools

- **HyperFrames (HeyGen):** write a video as an HTML page, render it to MP4, with about 470 ready-made blocks and
  components (captions, transitions, motion graphics), a linter and a preview. Our engine already works the same way
  (HTML scenes, every frame a function of time, Playwright, ffmpeg), so it is an add-on, not a rebuild. Its
  `reverse-any-video` skill can rebuild a video's structure as an editable project: use it to **study** the structure and
  timing of a winning video in MTG's niche, never to copy someone's content or look. Its media skill can make HeyGen
  voiceovers: for MTG only MTG Master Voice V3, and only after he approves the credits.
  **Tested with MTG's OK on 26 Nov 2026:** a 13.5 s silent ClickBaitPays hook (`tools/hyperframes/cbp-hook-test/`,
  README there) rendered at 1080 x 1920 in 41 s. Run every command with `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1
  HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium HYPERFRAMES_CHROME_SANDBOX=0`, pinned `npx -y hyperframes@0.9.92`.
  Never run its `publish` command (uploads to HeyGen) or its usage beacon (`events`) without MTG's OK. Its best part is
  `check`: it caught words under the TikTok and Reels buttons, closing lines on screen too briefly, a 26 px line and
  two contrast failures before render. Gotcha: a block variable named `accent` also becomes the CSS variable `--accent`,
  overriding the brand colour (the text came out pure blue); pick the block option that reads `--brand` instead and set
  `--brand` to the site's colour. Registry blocks are sized for 16:9; after `add`, edit them for vertical (they are
  ordinary source in the project).
- **Herk Edit Kit:** made for videos where the creator films himself (cuts stutters, retakes and pauses, with review
  before each cut). MTG records his screen silently and the voice is V3, and we already cut from transcripts
  (`tools/invite-horizontal/`), so it is not needed now. Revisit if MTG starts filming himself talking to camera.

## Not taken, and why

- "No intro or outro card": MTG's signature ending is a standing rule.
- Nate's paid services (ElevenLabs transcription, Kie.ai generation): we transcribe locally with faster-whisper, free.
