# The ultimate PDF companion

Some visitors would rather download a PDF than browse. Each website ends with one PDF that gives them enough to
understand everything, and that sends them back to the site, the videos and MTG's sign-up links with tappable
buttons. It is a map and a launcher, not a copy of the website: short summaries, the key picture or number for each
topic, and buttons.

## When

Last, once the site's pages and explainer videos are finished and approved, because the PDF links to them. Rebuild it
whenever a page, a video or a link changes, and put the version date on the cover.

## Structure

1. **Cover:** the site's name and promise in one line, MTG 👑 | Your Digital Architect, the date, and a big
   "Start here" button that opens the site's main page.
2. **How to use this guide:** one short paragraph ("tap any button to open the page or video"), plus the risk line the
   site requires.
3. **One spread per topic**, in the site's own order (for JetUP: the simple picture, 70/30, exposure and Amplify,
   the 5 checks, the sign-up steps, the promo, the partner plan, the tools, the BIX Card). Each has:
   - a 3 to 5 line summary in plain language and the one key number or picture,
   - a **"Watch the explainer"** button with the video's thumbnail, linking to the page section where the video plays
     (or the video file if MTG prefers),
   - an **"Open this page"** button linking to the exact section (use the section's `#id` anchor),
   - where it fits, the action button with MTG's real link for that step ("Get my Partner link", "Sign up").
4. **Step-by-step checklist** for getting started, each step with a button to its part of the tutorial.
5. **Risks and honesty page:** the site's disclaimer points in short form, with a button to the full disclaimer.
6. **All links in one place:** every button again as a simple list, so nothing is hard to find.
7. **Back cover:** the main call to action with MTG's referral link, "Join the tribe" (WhatsApp), Telegram, and the
   slogan exactly: Let's Get This Crypto! 💪

## Design and buttons

- Match the website's look (colours, fonts, the same icons and emojis), A4 portrait, one column, large type, so it reads
  well on a phone screen and also prints.
- Buttons are real links: rounded shapes at least 12 mm tall with clear labels, and the full address written small
  under each important one, for printed copies.
- Images compressed so the file stays small (aim under about 8 MB). Fonts embedded. Document title and language set.
- Same brand rules as everything else: no em or en dashes, the slogan exact, no personal data, no invented figures.

## How to build it

Write the PDF as an HTML page with print styles (one section per page, `break-before: page`), using the site's own CSS
tokens, then print it to PDF with headless Chromium (Playwright `page.pdf()`), which keeps every link tappable. This
needs no paid service and the result matches the website exactly.

## Check before showing MTG

Run `python3 scripts/check_pdf_links.py <file.pdf> [--online]`. It lists every link on every page, flags pages with no
button, placeholder or empty links, any em or en dashes in the text, and with `--online` checks that each web address
answers. Fix everything it reports, open the PDF and look at each page, then send it to MTG as a preview. Once he
approves, add it to the site's downloads page and link it from the main page.
