# Canton Weekly (mtgtribe.com/canton-weekly/)

Every Sunday the "Canton CC Weekly Report" scheduled task:
1. Researches the week and writes `tools/canton-weekly/data/YYYY-MM-DD.json` (copy the previous week's file as the shape).
   Fill in its `guides` block too: it refreshes the snapshot numbers on /cc/ and /cntn/ in step 4.
   Do step 4 even if HeyGen is out of credits: skip steps 2 and 3, leave out `"video"` and the page shows "Video coming soon".
1b. **Prepare the video data (MTG, 24 Nov 2026), BEFORE the narration:**
   `python3 tools/canton-weekly/prepare.py tools/canton-weekly/data/DATE.json`. It adds `"candles"` (Kraken CC/USD daily
   candles with MA20, MA50, RSI 14 and volume, for the video's 3D candlestick chart) and puts MTG's **fixed scenes** into
   `video_script`, word for word (the wording lives in prepare.py; never rewrite it per week):
   - after the fundamentals: `"burn"` (the universal burn, CIP-0129: what it is, when it starts, why it is positive for
     CC) and `"halving"` (the Canton Coin minting curve: the next halving in late summer 2029, the one after around 2034,
     what each does, why it is positive for the price);
   - before the outro: `"tribe"` (thank everyone in the MTG TRIBE WhatsApp group, invite everyone else to
     mtgtribe.com/group, where updates are posted first), `"streams"` (MTG buys CC and CNTN with the cash flow from his
     income streams: mtgtribe.com, Dashboard, Menu, Income streams, each stream named and highlighted one by one, then
     "test drive one") and the **Bellver Card ad** (`"bellver"`).
   The streams are read from the Income streams list of the dashboard menu (dashboard/index.html), and video.py takes
   fresh phone screenshots of this checkout's mtgtribe.com for that scene (menu_capture.js), so a new stream appears on
   its own. Streams MTG no longer wants named are listed in `EXCLUDE_STREAMS` in prepare.py (ALTRUVA since
   24 Nov 2026): they are left out of the script and hidden in the menu screenshots. Because the narration is made from `video_script`, all of this is in MTG's voice. The fixed scenes add about
   1 minute 45 seconds, so **keep the week's own scenes (intro to fundamentals, guides, outro) short and to the point**:
   about 1 minute 30 seconds together, the whole video about 3 minutes 15 seconds at most. This replaces the older "under about
   2 minutes" in the task prompt (MTG, 24 Nov 2026): never shorten or leave out a fixed scene to save time. Do not mention the universal
   burn or the halving again in the fundamentals scene unless there is real news on them that week.
   **Facts check:** if prepare.py prints `"warnings"` about the burn or halving facts being dated (from 1 January 2027 for
   the burn, 1 June 2029 for the halving), check the sources named in prepare.py (CIP-0129 and the Canton CIPs list,
   docs.canton.network), update the BURN or HALVING wording (spoken text and caption, same number of sentences) and
   video.py `HALVING_BARS` if needed, and tell MTG what changed in the notification. Also do this any week the news says
   universal burn went live or its dates moved.
   Needs api.kraken.com (public, no key). If Kraken cannot be reached it stops: say so in the report and carry on; the
   video then falls back to the old line chart, still with the ad if you add the scene by running it again later.
   video.py prints `"warnings"` when candles, the ad or any fixed scene is missing, or when the menu screenshots could not
   be taken (it then uses the stored copies in `tools/canton-weekly/assets/menu/`): fix that before publishing, and refresh
   the stored copies with `node tools/canton-weekly/menu_capture.js http://127.0.0.1:PORT tools/canton-weekly/assets/menu`
   (serve the repo with `python3 -m http.server PORT`) whenever the menu changes.
   Chart rules (MTG): candlesticks, MA20 (gold), MA50 (blue), volume and RSI 14, in a 3D tilted panel, clean: **no
   Bollinger Bands** (too busy). The trend and levels scenes use it; support and resistance are drawn on the levels scene.
2. Narration: HeyGen voice "MTG Master Voice V3" (65f1b9ff3f1e418496de5715a801e7dd, MTG's voice since 10 Nov 2026; V2 is
   retired), one create_speech call with the `video_script` texts joined by a blank line (no break tags: V3 does not
   support them). HeyGen returns WAV: save it as `/tmp/narration.wav` and pass that path to video.py (do not commit it).
3. Video: `python3 tools/canton-weekly/video.py tools/canton-weekly/data/DATE.json /tmp/narration.wav /tmp/they-call-me-mtg.mp3`
   (closing track: HeyGen asset aef5170534fa4430b6789ea5cd7335c0, download its url with get_asset; never commit it, it is MTG's own song).
   Then add `"video": {"src": "video.mp4", "poster": "poster.jpg", "title": "...", "duration_iso": "PT1M45S"}` to the JSON.
3b. Thumbnail (MTG, 8 Nov 2026), always AFTER video.py, which writes a plain poster.jpg from a video frame (that frame
   can catch the price mid-animation, so never keep it): add a `"thumb"` block to the JSON, for example
   `"thumb": {"hook": "Holding support after the SEC letter", "move": "-5%", "move_label": "this week"}` (the hook is a
   short, factual line from this week's report, no hype), then run
   `python3 tools/canton-weekly/thumb.py tools/canton-weekly/data/DATE.json`. It overwrites canton-weekly/DATE/poster.jpg
   with the designed cover: official Canton logo (unchanged file, assets/canton/), the price, the weekly move, the hook,
   the week's chart and MTG's gold-ringed circle photo. Open the poster and check the price matches the report.
   The page shows it under a gold play button (build.py `video_block`), with the Canton trademark note under the video.
   thumb.py also writes `canton-weekly/DATE/og.jpg`, the report's own social preview (1200x630: the price, the weekly
   move, the hook, the address; MTG, 9 Nov 2026). Open it and check the price too. A week without a video: run
   `python3 tools/canton-weekly/thumb.py tools/canton-weekly/data/DATE.json --og-only` so the report still gets its preview.
   build.py uses og.jpg when it exists, otherwise the hub's preview (`assets/og/canton-weekly.jpg`).
4. Pages: `python3 tools/canton-weekly/build.py tools/canton-weekly/data/DATE.json`
   (writes canton-weekly/DATE/, rebuilds the hub canton-weekly/index.html, updates sitemap-home.xml (adds the new report and gives today's date,
   South African time, as `<lastmod>` to every page the run changed, so Google knows to crawl them again) and, for the
   newest report only, refreshes the `data-snap` numbers on /cc/ and /cntn/ from the `guides` block).
5. Commit to a `claude/canton-weekly-DATE` branch, push it, then publish on your own (MTG, 8 Nov 2026, confirmed 22 Nov 2026:
   "I do want you to publish these weekly reports automatically"). Do not wait for "publish". Run these as four separate
   commands, exactly as written, so they match the allow rules in `.claude/settings.json`:
   `git fetch origin main`, `git checkout -B main origin/main`, `git merge --no-edit claude/canton-weekly-DATE`,
   `git push origin main`. Then confirm the four URLs load and send MTG the "it is live" notification.
   If the push is still refused, do not work around it: notify MTG that the report is ready on its branch.

## Posting pack (MTG, 22 Nov 2026)

With every report, give MTG the YouTube thumbnail (canton-weekly/DATE/poster.jpg), the WhatsApp image (og.jpg), a YouTube
title (under 70 characters), description and tags, a WhatsApp message and a WhatsApp Status caption. Lay every description
out with pointing fingers and spaces as the "post descriptions" rule in `.claude/CLAUDE.md` shows: label, blank line,
👉 link on its own line, blank line.

## Prices on the guides

- /cc/ loads the live Canton Coin price from CoinGecko in the visitor's browser (no credits used). If that fails,
  it shows the `guides.cc` snapshot, and once that is over 14 days old a "may be out of date" line links to CoinGecko.
- /cntn/ shows the `guides.cntn` snapshot. Once `guides.cntn.date` is over 14 days old, a notice links to Nasdaq.com.
- Live CNTN price: /cntn/, /cc/, the hub and every report show a "CNTN live price" card (TradingView mini chart, filled in the
  browser by `/assets/tribe/cntn-live.js`, which the master page head loads). The report and hub cards come from `CNTN_CARD` in
  build.py. On /cntn/ the card's fallback line reuses the `guides.cntn` snapshot (`data-snap="price"` and `price_date`).
- Live CC price: /cc/, the hub ("Canton Coin right now") and every report (Snapshot, "CC right now") show a "CC live price"
  card: the same script with data-symbol="KRAKEN:CCUSD". The report and hub cards come from `CC_CARD` in build.py.
- Bellver Card promo (MTG, 8 Nov 2026): one slim card-image promo just above the footer of every Canton page (it comes with the
  footer copied from cntn/index.html). MTG removed the big mid-page version: keep only the slim one. Styles:
  /assets/tribe/bellver-promo.css. The card, ORDER YOUR CRYPTO CARD and BECOME A PARTNER open bellveraffiliates.com.
- Report navigation (MTG, 8 Nov 2026): every report has a Previous week / All reports / Next week bar near the top and
  previous and next week cards plus First and Latest links at the bottom. The hub, /cc/ and /cntn/ show a Latest /
  First / All reports strip (between the `canton-weekly-nav` markers on the guides). build.py rebuilds every report on
  every run, so last week's report gets its Next week link as soon as the new one is built. Styles: canton-nav.css.
- If the weekly task stops (cancelled, or out of Claude credits), nothing breaks: the guides keep the last numbers and
  the notices tell visitors to check a live price.

`guides` shape (values are HTML, dates are the day the numbers are from):

    "guides": {
      "cc":   {"date": "2026-11-01", "date_h": "1 November 2026", "price": "<b>$0.0962</b>",
               "chg": "About -5% / about -21%", "mcap": "About $3.85 billion (top 30)",
               "ath": "$0.1942 on 3 February 2026, about double today's price", "supply": "39.97 billion CC, no maximum, still growing"},
      "cntn": {"date": "2026-10-30", "price": "$1.98", "price_date": "30 October 2026", "range": "$1.66 to $6.89"}
    }

## Official website links

`official_links.py` holds the verified official site for every company, exchange, wallet and tool we name.
build.py links the first mention of each name in every section of the reports, the hub and both guides.
Before naming something new in a report, add it there with its official address, checked against
cantonecosystem.com (Canton Network's official directory) or the company's own site. Never guess an address.

Design: everything reuses cntn/index.html (the master page). No em or en dashes anywhere.

## Standing publishing rule (MTG, 8 November 2026)

From 8 November 2026 the weekly task publishes on its own: build, commit to the `claude/canton-weekly-DATE` branch, merge to
`main`, push, confirm the four URLs load, then send MTG a notification that the report is live. MTG checks it afterwards.
