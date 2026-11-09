# Social previews: one designed image per page

MTG, 9 November 2026: "When I share any link, it always shows the same thumbnail... customize the preview thumbnail
that appears when I paste any link on socials according to what the page is... optimized for click-through rate, so
that when people see it, they just can't help but tap on it."

## What every page gets

- Its own `og:image`: 1200x630 JPEG, under 200 KB (WhatsApp drops previews over about 300 KB), with
  `og:image:secure_url`, `og:image:type`, `og:image:width` and `og:image:height` matching the real file, `og:image:alt`,
  `twitter:card` = `summary_large_image` and the same `twitter:image`. Add `?v=<hash of the file>` to the image address
  so caches refresh when it changes.
- Redirect links (short links, the WhatsApp group link) carry tags too: the crawler reads the redirect page itself.
  A short link to a guide reuses that guide's preview.

## The design formula

1. **Headline (left, huge):** what the page gives the visitor in 2 or 3 short lines, about 6 words. Real numbers where
   they exist (the $100 promo, 6 parts, 21 questions, 24 words). Curiosity and benefit, never hype.
2. **One visual (right):** the subject itself, built from the page: the phone with the steps, the account cards, the
   calculator with a worked example, the checklist, the ranked list, the week's price and chart. One focal point.
3. **The address pill (bottom left):** the exact page address, bright, with a play arrow. It tells people where the tap lands.
4. **Context:** a small eyebrow pill and the brand mark: the opportunity's logo on its pages (no photo of MTG where his
   videos use the logo), MTG's whole photo in a gold-ringed circle on MTG TRIBE pages, third-party logos as supplied and
   kept apart from MTG's branding.
5. **Readable at phone size:** check the set at about 330 px wide (a WhatsApp bubble). The headline and the visual must
   read; small print is only a bonus.
6. **Honest:** no income promises, no fake balances, chats or testimonials, examples labelled as examples, no "best
   ever". No em or en dashes.

## How it is done on mtgtribe.com

`tools/og/make_og.py` (HTML templates rendered with Playwright, auto-fitted headlines), `tools/og/check_og.py` (checks
every page), `tools/og/README.md`. Weekly reports make their own preview with the week's numbers
(`tools/canton-weekly/thumb.py`). Build a contact sheet and a phone-size mock, look at every image yourself, then publish.
After publishing, check each live image loads (200, image/jpeg). Tell MTG that chats which already had a link keep the old
preview, and that Facebook's Sharing Debugger refreshes its cache.
