# JetUP explainer #10: Know your numbers, the Exposure Calculator (14 Nov 2026)

MTG asked for the next explainer on 14 Nov 2026 ("Let's cook the next explainer video"): #10 in
`tools/learning-system/PLAN.md`, the Exposure Calculator walkthrough. MTG approved six new lines the same day ("Yes,
record (1 credit)"): recorded in one request in MTG Master Voice V3, 44.8 s, 1 credit (42 before, 41 after).
**Being built as a preview; not published.**

16:9, 1920x1080, 25 fps, captions burned in, the JetUP logo disc (never MTG's photo), the series' glass style, only the
four signature sounds. Calm, positive copy: know your numbers before you start (MTG, 8 and 9 Nov 2026: inform, never
frighten). Explainer #3 (Amplify 24x) already shows the calculator for about 8 s; this one walks through it tap by tap.

## The picture

Checking the map before a road trip: you know the distance before you drive. The calculator is your map for Amplify.
The rest of the video is the real calculator page (mtgtribe.com/jetup/tools/exposure-calculator/) in a laptop frame,
tap by tap: the training example ($150 + $100 bonus, 24x), the balance $250 and the exposure $6,000, the three fields,
the price move slider (1% on $6,000 is $60, both ways), the two last results (2.5% equals your own $150, 4.17% equals
the whole balance), the page's own loss limit note, and the recap.

## Lines (plan.json)

New (V3, `voice/ex10v3.flac`): nhook, nex, nown, ndrag, nlines, nrecap. Banked (0 credits): six, expo, swings
(sign-up training t1 and 5 Checks), nlimit (explainer #3's V3 line) from `explainers/ex3-pack/`; the greeting, close,
fair-play lines and signature ending from `explainers/ex4-pack/`. Speech-to-text hears every line as written (numbers
as digits). HeyGen's word times for lines 2 to 6 ran 0.15 to 0.2 s ahead of the audio: shifted in `lines_ex10.py` (ALIGN).

Facts: the calculator page itself (`jetup/_build/pages_tools.py` build_exposure) and `jetup-facts.md` (24x Amplify,
the loss limit 10%, 5% with a community token). No return figures.
