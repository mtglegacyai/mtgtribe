# Sideways-scroll check (MTG, 6 November 2026)

MTG: no section or part of any page may make a visitor scroll sideways on a smartphone. `hscroll.js` checks every
page for three things, at phone, tablet and small laptop widths, at normal text size and with Android's larger text (130%):

1. the page itself scrolling sideways,
2. any box inside the page that scrolls sideways (this is what tables used to do),
3. visible text cut off by the screen edge.

## Run it

Serve the repo locally (any static server, for example `http-server . -p 8765 -c-1`), then:

```bash
find . -name "*.html" -not -path "./tools/*" -not -path "./.git/*" -not -path "*/_build/*" | sed 's#^\./##' | sort > /tmp/pages.txt
```

```bash
node tools/qa/hscroll.js /tmp/pages.txt /tmp/hscroll.json 320,360,375,390,412,430,480,540,600,641,700,768,820,1024 1,1.3
```

Add 880, 912 and 960 for the widths between tablets and small laptops. To check another address (for example the live site),
put `BASE=https://mtgtribe.com/` in front of the command.

The check measures against the real screen width (`documentElement.clientWidth`). Until 11 Nov 2026 it used `innerWidth`,
which grows with a page that is too wide in phone mode, so a page wider than the screen was never reported.

It prints how many page views had a problem and writes the details to the JSON file. Things that are fine by design
and can be ignored: screen-reader-only text (`.sr`, `caption.sr`), the moving ticker tape on /jetup/ (`.tape`) and
ALTRUVA video titles that end in "..." (`.vt`). Text clipped to nothing for screen readers (`clip:rect(0 0 0 0)`) is skipped by the check
itself. `/group/` forwards to WhatsApp, so what the check measures there is WhatsApp's own page, not ours.

## How tables stay on the screen

- JetUP and ALTRUVA pages: the page builders run `phone_tables.py` (in `jetup/_build/` and `altruva/_build/build/`), which
  copies each column name onto its cells. Cells wrap at every size. A small script in `jetup.js` and `altruva.js` stacks
  any table that would not fit its box, and on phones tables with long text or 3 or more columns always stack.
  Tables that fit stay normal tables, so desktop looks the same as before.
- Canton guides and weekly reports: their own stacked layout now applies up to 640 px (the weekly builder copies it
  from `cntn/index.html`).

# Back to the video when it ends (MTG, 10 Nov 2026)

`/assets/video-return.js` brings the page back to exactly where the visitor pressed play when a video ends (pop-up,
inline and playlist players, phone and computer, full screen too). Every page with a video loads it. Check it with:

```bash
node tools/qa/video-return-test.js http://127.0.0.1:8766
```

It needs a static server that answers range requests (videos must seek), for example `npx http-server . -p 8766`.
Each case runs without and with the script; with it, every video's cover must come back to the same place on screen.

