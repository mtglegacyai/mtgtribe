# JetUP explainer #6: "The partner plan: the rule most people miss", 11 Nov 2026

MTG asked for the next explainer on 11 Nov 2026 ("Let's make the next explainer video"): #6 in
`tools/learning-system/PLAN.md`. He approved nine new lines in **MTG Master Voice V3** (`65f1b9ff3f1e418496de5715a801e7dd`):
one request, no model or engine override, one paragraph per pause, 1 credit (49 left). Banked on `jetup-video-work` as
`jetup-work/voice-bank/explainers/ex6v3.flac`; the cut lines are in `ex6-pack/`. Checked word for word, levelled to -18.5 LUFS.

The picture: a building with ten glass floors (the levels) and an access card. $250 of active trading opens floors 1 to 3;
1 to 3 direct partners: still 3; from the 4th direct partner each new one opens the next floor; 10 direct partners open all
10. Then what open floors pay (lot commission $2 / $1 / $0.50, up to $8.00 per lot, from real trading; Profit Share 1.5% on
every open level, paid from the 30% share), client start ($155) or partner ($250, check the partner account), the rule in
three lines, and "Now it's your turn". Glass style as approved for the JetUP pages (10 Nov 2026).

- `lines_ex6.py`: cuts the nine new lines from the V3 take (word times from HeyGen's reply) and gathers the shared greeting,
  close and signature lines from explainers #1 and #2.
- `make_ex6.py`: voice placement, captions ($250, $155, $8, $2, $1, 1.5%, 30%), cues, the signature ending's cues
  (`links=False`, Next: the 70/30 split), body sounds (whoosh, tick, pop, click).
- `stage/`: scenes: hook (10 levels, only 3 open); hi; what's a level (you, level 1 direct partners, level 2, ten deep);
  how the floors open (access card, $250, the direct partner counter, all 10 open); lot commission bars; Profit Share
  chips and the 30% share; client or partner; the rule; now it's your turn.
- `cover.html`, `shoot_cover.js`: the 16:9 cover ("EXPLAINER · 2:18", "THE PARTNER PLAN", ten floors, three lit).
- Build: `tools/video-signature/build_part.sh <dir> <out.mp4>`; QA: `tools/video-signature/qa_new.py <dir> <out.mp4>`.
  Preview of 11 Nov 2026: 138.36 s, 1920x1080, 25 fps, -14.0 LUFS, true peak -2.6 dBFS, closing track from 87.0 s.
- Facts checked against `tools/learning-system/jetup-facts.md` (partner plan, levels open, client start) and JetUP's
  business plan and "How partners grow" one-pager (Oct 2026). JetUP's figures only, no income promises.

## To publish once MTG approves

`jetup/media/jetup-explainer-partner-plan.mp4`, covers `jetup/img/cover-explainer-partner-plan.jpg` and `.webp`, a video
key in `jetup/_build/layout.py` (dur '2:18', iso 'PT2M18S'), placed at the top of the Partner Plan page ("The rule most
people miss") and on the Videos page, with VideoObject data. Run the feature checks, the sideways-scroll check and
`tools/og/check_og.py`.

## On the site (11 Nov 2026)

MTG: "Put it live". `jetup/media/jetup-explainer-partner-plan.mp4`, covers `jetup/img/cover-explainer-partner-plan.jpg` and
`.webp`, video key `partnerplan` in `jetup/_build/layout.py`. Places: the top of the Partner Plan page (with VideoObject
data), the Videos page (after Amplify 24x), and a link from the FAQ answer "Do I have to build a team?". Placement script:
`ex6_site_edits.py`. Sitemap dates for the three pages: 2026-11-11.
