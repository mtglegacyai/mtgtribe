# Canton Weekly (mtgtribe.com/canton-weekly/)

Every Sunday the "Canton CC Weekly Report" scheduled task:
1. Researches the week and writes `tools/canton-weekly/data/YYYY-MM-DD.json` (copy the previous week's file as the shape).
2. Narration: HeyGen voice "MTG Master Voice V2" (3931c505632149ceb2bbfecf2778c09c), one create_speech call with the
   `video_script` texts joined by `<break time="0.4s"/>`. Save it as `/tmp/narration.mp3` (do not commit it).
3. Video: `python3 tools/canton-weekly/video.py tools/canton-weekly/data/DATE.json /tmp/narration.mp3 /tmp/they-call-me-mtg.mp3`
   (closing track: HeyGen asset aef5170534fa4430b6789ea5cd7335c0, download its url with get_asset; never commit it, it is MTG's own song).
   Then add `"video": {"src": "video.mp4", "poster": "poster.jpg", "title": "...", "duration_iso": "PT1M45S"}` to the JSON.
4. Pages: `python3 tools/canton-weekly/build.py tools/canton-weekly/data/DATE.json`
   (writes canton-weekly/DATE/, rebuilds the hub canton-weekly/index.html and updates sitemap-home.xml).
5. Commit to a `claude/canton-weekly-DATE` branch. Push to `main` only after MTG says "publish".

Design: everything reuses cntn/index.html (the master page). No em or en dashes anywhere.
