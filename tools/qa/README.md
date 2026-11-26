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
node tools/qa/hscroll.js /tmp/pages.txt /tmp/hscroll.json 320,360,375,384,390,412,430,480,540,600,641,700,768,820,1024 1,1.3
```

Add 880, 912 and 960 for the widths between tablets and small laptops. Keep 384 in the list: MTG's own phone shows pages 384 px wide (22 Nov 2026: a glow ring 6 px past the edge showed up only there, with large text). To check another address (for example the live site),
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

# Things lying on each other (MTG, 22 Nov 2026)

MTG: "the top right button that takes the visitor to the dashboard is overlapping the website title ... look for any other
areas ... that might have some objects overlapping each other." `overlap.js` finds text, icons, pictures and buttons whose
boxes overlap when they should not, line by line, at phone widths and with Android's larger text:

```bash
node tools/qa/overlap.js /tmp/pages.txt 320,360,375,384,390,412,430,768,1100 1,1.3
```

Designed overlays are not overlaps: a play button on its cover, a badge inside its card, a list that scrolls under a sticky
panel (`.md-bot` or `[data-scroll-under]`), the quick bar, anything marked `data-overlay`. It must print `0 with an overlap`.

# Back to the video when it ends (MTG, 10 Nov 2026)

`/assets/video-return.js` brings the page back to exactly where the visitor pressed play when a video ends (pop-up,
inline and playlist players, phone and computer, full screen too). Every page with a video loads it. Check it with:

```bash
node tools/qa/video-return-test.js http://127.0.0.1:8766
```

It needs a static server that answers range requests (videos must seek), for example `npx http-server . -p 8766`.
Each case runs without and with the script; with it, every video's cover must come back to the same place on screen.
To run only some cases, put part of their name in `ONLY`, for example `ONLY=BW node tools/qa/video-return-test.js http://127.0.0.1:8766`.


# The whole video, always (MTG, 16 Nov 2026)

MTG: "displayed in full, nothing hidden, but at the same time not too big ... even when they are maximized ... and the
close button is still there." `player-check.js` plays every video on /bw (in the page and in the pop-up) at 21 screen
sizes, phones upright and on their side, tablets and computers, and fails if anything is cut, covered or off screen:

- the picture is whole and on screen, under the site's top bar, and the frame around it too;
- the video is never cropped (`object-fit:contain`, no rounded corners) and the screen has the video's own shape;
- nothing lies on the picture (it samples 81 points on it);
- Full Screen and Close are there, on screen, big enough, and not on the picture, also in full screen, and the words
  "Full Screen" (or "Exit Full Screen") show on the button at every size;
- leaving full screen keeps the video playing; Close returns to the cover and leaves nothing behind;
- the play button cannot be missed: in the middle of every cover (or in the spot the cover names), wholly on the cover, at
  least 52 px wide.
- every video on the page is a 16:9 cover inside the laptop frame (MTG, 17 Nov 2026), not wider than the screen, and its
  picture has loaded; pressing a vertical video's cover must open the pop-up's phone (which gets all the checks above), and
  Close must bring the cover back.
- on a video's own page (`/bw/dashboard/tutorials/<name>/`), a time button is finger sized and starts the video at its second.

`PAGES=/bw/dashboard/tutorials/,/bw/ VPS=360x640,1366x768 node tools/qa/player-check.js` runs a part of it while you work.

```bash
node tools/qa/player-check.js
```

```bash
FALLBACK=1 node tools/qa/player-check.js
```

The second run is a browser without full screen for page elements (some in-app browsers): the player must cover the
window itself. Needs the same kind of server as above on port 8765 (`BASE=...` for another address); `VPS=360x640,740x360`
runs only those sizes; `SHOT=folder` saves pictures. It must print `0 failures` before MTG sees a preview.

The ClickBaitPays guide (/cbp) plays YouTube videos in the same player, so it has its own copy of this check:
`node tools/qa/cbp-player-check.js` (same options, same rules). YouTube does not play in the test browser, so the
check treats the YouTube player's box as the picture; it must print `0 failures` too.

# The Bitcoin Wealth guide (/bw): two more checks (16 Nov 2026)

```bash
python3 tools/qa/bw-static-scan.py
```

Reads every built /bw page: broken links and anchors, missing files, unclosed tags, duplicate ids, pictures without alt
or size, meta and social tags, JSON-LD, heading order, buttons without a name, dashes. It must print `0 findings`.

```bash
node tools/qa/bw-tools-test.js
```

Uses every interactive tool on a phone and on a computer with a fixed Bitcoin price, and checks the answers: the Bitcoin
to Rand converter (all three boxes, presets, own price, comma decimals, bad input), the slot calculator (slots 1, 5
and 12), the halving countdown, the glossary search, the fit check, the copy sheet, Mark as watched and the progress
ring, the menu, Back to top, the order form's WhatsApp message and the live slot price. It must print `0 failures`.


# Private preview link (MTG, 16 Nov 2026)

MTG: "I mean a live preview on a temporal web link." Before a /bw change goes live he gets a private link with the built
pages, to tap through on his phone. How:

1. In `bw/_build/build`: `import build; build.render_preview(SCR + '/out/preview')` (set `sys.argv = ['x']` first). It writes
   the whole guide with relative links: 26 pages, assets, covers and videos.
2. Give the main page a short `<title>` ("Bitcoin Wealth Guide").
3. The host takes no file over 15 MB and at most 64 MB in one go: make lighter copies of the long videos for the link only
   (the video under review stays the real file), and tell MTG which ones are lighter.
4. The host serves no `.ics` file and blocks scripts from other websites: leave the Zoom calendar file out, copy
   `assets/wa-message.js` and `assets/zoom-cta.js` into the copy's `assets/`, point the pages at them, and in that copy of
   `zoom-cta.js` set `var BW = true;` (the script reads the address to know it is a Bitcoin Wealth page).
5. Test the copy on a local server with range requests (play, auto close, buttons), then publish `index.html` with every
   other file as a supporting file.
6. Tell MTG what differs from the real site: live prices cannot load there, some videos are lighter copies, and the page sits
   inside a viewer, so Full Screen can behave differently. The link cannot be opened from the session: say the same files
   were tested locally, not that the link was tested.


## Private preview of pages outside /bw (26 Nov 2026)

For a change to mtgtribe.com, /jetup, /cbp or a few /bw pages (a stylesheet fix, a section), bundle just the changed pages:

```bash
python3 -I tools/qa/preview_bundle.py /home/user/mtgtribe <scratchpad>/preview "index.html,jetup/index.html,bw/dashboard/index.html"
```

It copies each page with the stylesheets, scripts, images and fonts it uses, rewrites the site's addresses to relative
links, sends links to pages outside the preview to the live site, and leaves videos out (it lists them). Then:

1. In the copy of `assets/zoom-cta.js`, drop the `^` from the `BW` and `JU` address checks (the private link has another
   address), as in step 4 above.
2. Write a short guide page as `<preview>/index.html`: what changed, before and after pictures (live site against the
   local build, at the same width), and a button into each page with what to look at.
3. Serve the folder locally and load every page at 360 px: no missing file except the videos, no script error, no
   sideways scroll. Then publish `index.html` with every other file as a supporting file, and tell MTG what differs.
