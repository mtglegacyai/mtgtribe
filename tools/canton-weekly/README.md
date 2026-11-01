# Canton Weekly (mtgtribe.com/canton-weekly/)

Every Sunday the "Canton CC Weekly Report" scheduled task:
1. Researches the week and writes `tools/canton-weekly/data/YYYY-MM-DD.json` (copy the previous week's file as the shape).
   Fill in its `guides` block too: it refreshes the snapshot numbers on /cc/ and /cntn/ in step 4.
   Do step 4 even if HeyGen is out of credits: skip steps 2 and 3, leave out `"video"` and the page shows "Video coming soon".
2. Narration: HeyGen voice "MTG Master Voice V2" (3931c505632149ceb2bbfecf2778c09c), one create_speech call with the
   `video_script` texts joined by `<break time="0.4s"/>`. Save it as `/tmp/narration.mp3` (do not commit it).
3. Video: `python3 tools/canton-weekly/video.py tools/canton-weekly/data/DATE.json /tmp/narration.mp3 /tmp/they-call-me-mtg.mp3`
   (closing track: HeyGen asset aef5170534fa4430b6789ea5cd7335c0, download its url with get_asset; never commit it, it is MTG's own song).
   Then add `"video": {"src": "video.mp4", "poster": "poster.jpg", "title": "...", "duration_iso": "PT1M45S"}` to the JSON.
4. Pages: `python3 tools/canton-weekly/build.py tools/canton-weekly/data/DATE.json`
   (writes canton-weekly/DATE/, rebuilds the hub canton-weekly/index.html, updates sitemap-home.xml and, for the
   newest report only, refreshes the `data-snap` numbers on /cc/ and /cntn/ from the `guides` block).
5. Commit to a `claude/canton-weekly-DATE` branch. Push to `main` only after MTG says "publish".

## Prices on the guides

- /cc/ loads the live Canton Coin price from CoinGecko in the visitor's browser (no credits used). If that fails,
  it shows the `guides.cc` snapshot, and once that is over 14 days old a "may be out of date" line links to CoinGecko.
- /cntn/ shows the `guides.cntn` snapshot. Once `guides.cntn.date` is over 14 days old, a notice links to Nasdaq.com.
- If the weekly task stops (cancelled, or out of Claude credits), nothing breaks: the guides keep the last numbers and
  the notices tell visitors to check a live price.

`guides` shape (values are HTML, dates are the day the numbers are from):

    "guides": {
      "cc":   {"date": "2026-11-01", "date_h": "1 November 2026", "price": "<b>$0.0962</b>",
               "chg": "About -5% / about -21%", "mcap": "About $3.85 billion (top 30)",
               "ath": "$0.1942 on 3 February 2026, about double today's price", "supply": "39.97 billion CC, no maximum, still growing"},
      "cntn": {"date": "2026-10-30", "price": "$1.98", "price_date": "30 October 2026", "range": "$1.66 to $6.89"}
    }

Design: everything reuses cntn/index.html (the master page). No em or en dashes anywhere.
