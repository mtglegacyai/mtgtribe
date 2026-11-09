# Social previews: one designed image per page (MTG, 9 Nov 2026)

> "When I share any link, it always shows the same thumbnail... customize the preview thumbnail that appears when I paste
> any link on socials according to what the page is... optimized for click-through rate." (MTG, 9 November 2026)

Every page on mtgtribe.com has its own `og:image` (WhatsApp, Facebook, X, Telegram, LinkedIn): 1200x630 JPEG, under
200 KB (WhatsApp skips images over about 300 KB), with `og:image:width/height/type/alt`, `og:image:secure_url` and the
same `twitter:image`.

## The formula (what makes people tap)

- **One big headline that says what the page gives you**, 2 or 3 short lines (Anton, auto-fitted): "Check first. Then
  start.", "5 checks before you start", "Exposure calculator". Numbers where they are real ($100, 4 steps, 21 questions).
- **One clear visual of the page's subject** on the right: the phone with the 6 parts, the $50 and $200 accounts, the
  70/30 bar, the ranked streams, the week's price. Legible at phone size (about 330 px wide).
- **The exact address the link opens** in a bright pill (signals "tap and you land here").
- A small eyebrow pill for context, and the brand: JetUP pages carry the JetUP logo disc (no photo of MTG, as in his
  JetUP videos); MTG TRIBE pages carry MTG's whole photo in a gold-ringed circle; Canton pages carry the official Canton
  logo on its own (never next to MTG's branding, never recoloured).
- Honest: no income promises, no fake balances or messages, examples labelled ("Example: a $10 profit"). No em or en dashes.

## Files

- `make_og.py`: the designs and the page list (`SPECS`). `python3 tools/og/make_og.py [slug ...]` writes
  `assets/og/<slug>.jpg` and `tools/og/sheet.jpg` (all of them on one sheet). Needs Playwright (Chromium) and the
  Google fonts.
- `check_og.py`: checks every page's tags (file exists, 1200x630, under 300 KB, declared size, twitter:image, og:url,
  no two pages with the same image). Run it before publishing.
- JetUP pages: `jetup/_build/layout.py` (`OG`, path to image and alt text), then `python3 jetup/_build/build.py`.
  A new JetUP page needs a spec here and a line in `OG`.
- MTG TRIBE dashboard and `/group/`: tags edited in `dashboard/index.html` and `group/index.html` (the old ALTRUVA
  builder in `altruva/_build` still names `og-group.jpg` for `/group/`: if that builder is ever run again, point it at
  `/assets/og/tribe-whatsapp.jpg`).
- Canton: the hub uses `assets/og/canton-weekly.jpg`; every weekly report makes its own `canton-weekly/<date>/og.jpg`
  with that week's price, move and hook (`tools/canton-weekly/thumb.py`, see its README).
- Already their own and kept: ALTRUVA's 25 pages (`altruva/img/og-*.jpg`), the home page (`assets/tribe/og-tribe.jpg`),
  `/cc/` and `/cntn/`. The two short Canton links reuse the preview of the guide they open. `/JetUpZoom/` keeps its
  event flyer.

## After publishing

WhatsApp reads the preview when someone pastes the link, so new shares show the new image. Chats that already had the
link keep the old preview. Facebook caches: paste the URL into developers.facebook.com/tools/debug and press "Scrape
Again". The `?v=` on each image address changes whenever the image changes, so caches refresh.
