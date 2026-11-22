# ClickBaitPays revamp (mtgtribe.com/cbp): plan and status

Source of truth: MTG's handoff brief (14 Nov 2026) plus the decisions below, which win over the brief.
Files here: `edit-maps-checked.md` (every recording checked against the brief's edit maps, corrected timings and extra
privacy cuts), `pif-narration.md` (MTG's narration from inside PIF.mp4).

Working rules for this project:
- This is the ClickBaitPays project only. Keep each of MTG's websites separate; do not bring other sites into
  ClickBaitPays work or chat unless MTG does.
- Nothing is scripted, voiced, pushed or published without MTG's approval. Preview first, always.
- No em dashes or en dashes anywhere.

---

## 1. MTG's decisions (15 Nov 2026)

| Topic | Decision |
|---|---|
| Security PIN | MTG has changed it. Both PIF moments (1:42 to 1:53 and about 2:13) are still cut or fully covered, field and keypad |
| HeyGen | MTG bought 500 credits. Voice: MTG Master Voice V3 only |
| Username | Leave it visible (it is the same as his public join code). Balances, earnings and other members' details are still hidden |
| Logo | The official ClickBaitPays logo takes the place of MTG's photo in videos and thumbnails |
| Join link | https://clickbaitpays.me/join.php?ref=mtgtraffic on every Join button |
| Shift AI | MTG has not joined. See section 4 |
| Endings | Both: discovered ClickBaitPays here, join with the Join buttons on this page; invited by someone, go back to that person's link |
| YouTube | Keep all 5 existing ClickBaitPays Us videos (Overview, Income & Commission Plan, Back Office Walkthrough, Q&A, Presentation) |
| Site scope | Small, lean, clean, as few pages as possible. Not a course. Answer: what is ClickBaitPays, how it works, how to join. Explainer and YouTube videos carry the detail |
| Copies (clones) | Buyers choose mtgtribe.com/cbp/name or clickbaitpaysus.com/name in the order form, like the Bitcoin Wealth form. R1,000 or $50 once-off, same payment methods (Rand by bank transfer, USDT BEP20, USDT TRC20) |
| Auto-sync | Yes: mtgtribe.com/cbp is the master that updates clickbaitpaysus.com automatically |
| Still to record | Withdrawal, back office (dashboard) tour, deposit: all coming |
| Explainers | Yes, including the 12-day click period plus the 7-day hold |
| Explainer music | "They Call Me MTG" |

### MTG's notes with the Level 4 recording (21 Nov 2026, these win)

| Topic | Decision |
|---|---|
| Hide in the video | MTG's username, his balances, and other members' ads (their titles, links and pages). His own campaign title and bellveraffiliates.com may stay. (This reverses "leave the username visible" of 15 Nov for this video; ask whether it applies to all ClickBaitPays videos) |
| Earnings example | Per click, per day, for 12 days: only on the website and in the members' tutorial, as the platform's own figures next to the risk line. Never on YouTube, TikTok or Facebook, so tutorials with it get a social version without it |
| Activation fees | Say the once-per-level activation fees support the company's sustainability (video and revamped site) |
| Titles | Campaign titles are 30 characters at most |
| Preview | Always show Preview before Confirm Purchase |
| Available balance | Withdraw, Pay It Forward (point to its tutorial), or buy another campaign |
| Repo privacy | This repo is public: never write MTG's balances, usernames or other members' details in notes |

---

## 2. Video lineup (PROPOSED, awaiting MTG)

**Superseded on 22 Nov 2026 by `tools/cbp/VIDEOS.md`** (new Tutorial 1 Create and protect your account, 8 tutorials, 6
explainers, the script standard). Kept below for history.

Tutorial E needs two versions: the members' version (website) with the earnings example, and a social version without it.

Tutorials, in watch order (a member's journey: look around, fund, first campaign, grow, cash out, advertise, help your team):

| # | Title | Source | Status |
|---|---|---|---|
| 1 | Your ClickBaitPays Back Office: A Quick Tour | to record | waiting for recording |
| 2 | How to Deposit USDT into ClickBaitPays | to record | waiting for recording |
| 3 | Your First Ad Campaign on a New Level: Buy It, Activate Earning, Click Your Daily Ads | Tutorial E, the Level 4 walkthrough (17:37, about 5 min usable, target 6 to 7 min); replaces Tutorial A, which stays as spare footage | ready to script (PROPOSED 21 Nov) |
| 4 | Buy Another Ad Campaign on a Level You Already Activated | Tutorial C (27:45, target 6 to 9 min) | ready to script |
| 5 | How to Request a Withdrawal | to record | waiting for recording |
| 6 | How to Create a Login Ad | Tutorial B (16:54, target 4 to 6 min) | ready to script |
| 7 | How to Pay It Forward: Send Funds to Another Member | Tutorial D (3:22, vertical, target 1:30 to 2:30) | ready to script |

Explainers (16:9, about 60 to 90 seconds each):

| # | Title | Answers |
|---|---|---|
| E1 | What Is ClickBaitPays? | Advertisers get traffic, viewers get paid |
| E2 | How to Join ClickBaitPays | Invitation only; Join buttons on this page, or the link of whoever invited you |
| E3 | How It Works: Levels, Activation and Earnings | 7 levels, one-time activation per level, the platform's own figures |
| E4 | The 12 + 7 Timeline | Click for 12 days, 7-day hold, then your Available Balance |
| Tour | How to Use This Website | Landing page hero; made last, once the site exists |

Fair-play join line in every video (works on MTG's page and on every copy): "Tap any Join button on this page.
Invited by someone else? Use their link."

---

## 3. Lean site map (PROPOSED, awaiting MTG)

| Page | What is on it |
|---|---|
| mtgtribe.com/cbp | Site tour video in the hero; What is ClickBaitPays (E1); How it works in 3 steps (E3, E4); How to join (E2) with Join buttons; the 5 YouTube videos; top FAQ; Dashboard button |
| mtgtribe.com/cbp/dashboard | Tutorials 1 to 7 in order, the explainers, MTG's standard dashboard layout (sidebar with collapse, GO HOME button) |
| mtgtribe.com/cbp/calculator | One calculator: campaign plus activation cost, the platform's own earnings figures, and the 12 + 7 release date |
| mtgtribe.com/cbpcopy | Order your own copy (address choice, R1,000 or $50, payment method, sends to WhatsApp) |
| mtgtribe.com/cbp/disclaimer | Disclaimer and privacy, one page |

- The old clickbaitpaysus.com pages redirect to the matching section, so old links never break. The old 32 USDT
  "request a copy" page is replaced by the new order form.
- Every page gets its own social preview image, `/assets/video-return.js`, and passes `tools/qa/hscroll.js`.

---

## 4. Shift AI (PROPOSED default)

MTG has not joined. Video 4 shows the last ad as just another member's ad, with every personal detail hidden and no
Shift AI mention or call to action, so the video is not held back. If MTG joins later, his Shift AI invite goes on the
website, not into the video, so nothing has to be re-rendered.

---

## 4a. ClickBaitPays logo (MTG, 21 Nov 2026)

MTG's new emblem (round, "ClickBaitPays, CLICK WATCH EARN", cursor with gold click waves) is the logo for all his
ClickBaitPays websites: mtgtribe.com/cbp, every copy, and clickbaitpaysus.com. It replaces the platform's cyan and pink
"C" mark that clickbaitpaysus.com uses today (assets/logo.png and assets/favicon.png, on 35 pages).

Files in `tools/cbp/brand/` (copy into the site's assets when building):

| File | Use |
|---|---|
| clickbaitpays-logo-original.jpg | Source, 640x640, never edit |
| favicon.ico, favicon-16.png, favicon-32.png | Browser tab icon, option A (full emblem) |
| favicon-cursor.ico, favicon-cursor-16.png, favicon-cursor-32.png | Browser tab icon, option B (cursor close-up, reads clearly at 16 px) |
| apple-touch-icon.png (180) | iPhone home screen |
| icon-192.png, icon-512.png, icon-maskable-512.png | Android home screen and the web app manifest |
| clickbaitpays-logo-256.webp, clickbaitpays-logo-640.webp | Logo on pages |
| clickbaitpays-logo-disc-256.webp | Round header logo |
| clickbaitpays-logo-disc-video.png | Videos: greeting disc, top-bar disc, thumbnails, end card (gold ring added in the video) |

Where it goes: browser tab and home screen icons, page header, every page's social preview image, the order form, the
videos (in place of MTG's photo) and the PDF companion cover. Preview: `tools/cbp/brand-preview.png`.
Waiting on MTG: tab icon A or B; this emblem in the videos (yes or no); swap it onto the live clickbaitpaysus.com now
or with the rebuild.

---

## 5. Facts to re-check on the live site before publishing

- Level 6 campaign price 1,200 USDT (seen in Tutorial A at 3:45), Level 7 2,400 USDT (official FAQ).
- Level 2 completed campaigns earn 101.74 USDT on the dashboard; the current clickbaitpaysus.com calculator uses 101.70.
- Withdrawal fee (current site data says 10 percent) and maximum active campaigns (current site data says 3).

## 6. Next steps

1. MTG approves (or changes) the video lineup and the site map.
2. MTG switches to the highest model and effort, then Script 1 (Video 3) is written for approval.
3. Scripts for Videos 4, 6 and 7, one at a time, each approved before voicing.
4. Voice (V3), privacy-masked edit, preview to MTG, fix, final render.
5. Build the lean site and the order form, preview, publish only on MTG's approval, then set up the auto-sync
   (needs push access to MusaTheGiant/clickbaitpays).

---

## 7. Open questions answered (22 Nov 2026: MTG asked Claude to decide)

| Question | Decision |
|---|---|
| Video 3 | The Level 4 walkthrough (Tutorial E) replaces Tutorial A; A stays as spare footage |
| Preview step in Video 3 | Use the real Preview clip of the same link from Tutorial C (in E the Preview tab stayed blank) |
| Privacy in every ClickBaitPays video | Hide MTG's username, his balances and other members' ads (titles, links, pages), in all videos |
| Browser tab icon | Option B, the cursor close-up (16 and 32 px); the full emblem everywhere else, videos included |
| Logo on clickbaitpaysus.com | Arrives with the update from mtgtribe.com/cbp, not before |
| Shift AI | Hidden in Video 4, no mention |
| Site | The lean 5-page site (section 3) is approved |

## 8. First website build (22 Nov 2026, went live the same day; replaced by section 9)

Built with `python3 cbp/_build/build.py` (pages) and `python3 cbp/_build/og.py` (social previews, needs Playwright).
Every fact, price, link and video lives once in the CONFIG block of `cbp/_build/build.py`.

| Page | Address | Notes |
|---|---|---|
| Landing | /cbp/ | Hero with site tour placeholder, what it is (E1), how it works in 5 steps + 12+7 timeline (E3, E4), the 7 levels table, Login Ads vs Ad Campaigns, how to join (E2), tutorials teaser, 5 YouTube videos, 12-question FAQ, final call to action |
| Dashboard | /cbp/dashboard/ | MTG Dashboard Standard (shared mtg-dash.css/js) in ClickBaitPays colours; site tour, daily routine, tutorials 1 to 7, explainers, YouTube |
| Calculator | /cbp/calculator/ | Pay today, clicks a day, earned per click day, platform campaign total, release date (first click day + 18 days), net after the 10% withdrawal fee |
| Disclaimer and privacy | /cbp/disclaimer/ | Independent guide, referral disclosure (10%), figures, risk, privacy |
| Order a copy | /cbpcopy/ | R1,000 or $50, pay after it is built, 5 free edits, address choice, Rand / USDT BEP20 / USDT TRC20, sends to WhatsApp, stores nothing |

Videos: every slot is a placeholder in a laptop frame (16:9) or slim gold phone frame (9:16, Tutorial 7). To make one
playable, set its `src` and `poster` in CONFIG and rebuild. The pop-up player closes itself at the end and returns the
visitor to where they pressed play (YouTube through the IFrame API on youtube-nocookie.com; MP4 through /assets/video-return.js).

SEO and conversion: unique title (51 to 60 characters) and description (155 to 159) per page, canonical, Open Graph and
X cards with a designed 1200x630 preview per page, JSON-LD (Person, WebSite, WebPage, FAQPage, HowTo, ItemList,
WebApplication, Product with ZAR and USD offers, breadcrumbs), /cbp/sitemap.xml (added to /sitemap.xml and robots.txt),
/cbp/llms.txt (and a section in /llms.txt), web app manifest, self-hosted YouTube thumbnails, Join buttons with
rel="sponsored", sticky Join bar on phones, fair-play line next to every Join button, calm info notes, one risk line.

Checks run on 22 Nov 2026 (local server): tools/qa/hscroll.js at 17 widths (320 to 1024) x 2 text sizes, 0 problems in
170 page views; tools/og/check_og.py, all 5 pages OK; 43 functional browser tests pass (menus, sticky bar, video pop-up
open, close, scroll return and focus, calculator maths and edge cases, order form validation and WhatsApp message,
dashboard collapse and drawer, JSON-LD parses, internal links, anchors and images); no browser console errors; no em or
en dashes (the build refuses them). Not run yet: tools/qa/video-return-test.js (needs the first real video), Lighthouse.

Before going live: MTG approves the preview; re-check level figures on the live site; decide the canonical between
mtgtribe.com/cbp and clickbaitpaysus.com before the sync (recommendation: mtgtribe.com/cbp is canonical, the copy on
clickbaitpaysus.com points its canonical to it); link /cbp/ from the mtgtribe.com home and tribe dashboard (today the
ClickBaitPays card points to clickbaitpaysus.com); then the auto-sync to clickbaitpaysus.com (needs push access to
MusaTheGiant/clickbaitpays) with redirects from its 30 old pages.

---

## 9. The short-page layout (MTG, 22 Nov 2026)

MTG on the first layout: "the pages are so long ... The home page is supposed to have only 3 videos: the welcome video, the
income strategy, and the dashboard walkthrough. Then after that, you just redirect people to the dashboard ... Each page
must target one section, one idea at a time. And if there's a video relevant to that, put the video on that page ... the
navigation arrows back and forward, up and down." And the laptop frame had to match /bw (slim, thin gold rim).

What changed (builder: `cbp/_build/build.py`; covers: `covers.py`; previews: `og.py`):

| Part | Now |
|---|---|
| Main page /cbp/ | Hero, then exactly 3 videos from the ClickBaitPays Us YouTube channel: Welcome to ClickBaitPays (5:51), Income Strategy and Commission Plan (7:37), Back Office Walkthrough (11:26). Then the way into the dashboard (6 topic tiles). About a quarter of the old length |
| Dashboard | 21 short pages in the menu order (`NAV`): Start Here (Welcome, What Is ClickBaitPays?, How It Works, How To Join), Levels And Earnings (The 7 Levels, The 12 + 7 Timeline, Income Strategy, Calculator), Every Day (Your Daily Routine), Tutorials (All Tutorials, Tutorials 1 to 7, each its own page with its steps in writing), Help (Video Library, FAQ with the live Q&A, Your Own Copy, Disclaimer) |
| Navigation | Previous and Next arrows beside every page heading (with "5 / 21"), the Previous and Next pager at the bottom, the menu, and the floating Up and Down buttons (Down: the next part of the page; they step aside over a video) |
| Player | The /bw player (`.pl`): slim laptop with a thin gold-titanium rim, Full Screen and Close in the bar above the picture, YouTube plays in place from youtube-nocookie.com (YouTube's own full-screen button off), closes itself at the end and puts the page back where play was pressed. 9:16 videos open the pop-up's phone |
| Covers | Every video has a designed 16:9 cover (src/v, middle kept clear for the play button). A video still being made shows "Coming soon" or "Being recorded" where the play button will be |
| Videos per page | What Is ClickBaitPays: Welcome. How It Works: the 14 Sept presentation. Income Strategy: the strategy video. Tutorial 1: the Back Office Walkthrough until MTG's own tour is recorded. FAQ: the 29 Aug live Q&A. The rest wait for MTG's explainers and tutorials (placeholders) |
| Old links | The old one-page anchors (/cbp/#levels, /cbp/dashboard/#t5 ...) forward to the topic's page |

To make a placeholder playable: give its entry in `V` a `yt` (YouTube id) or `src` (video file) and its `secs`, remove
`status`, draw a cover in `covers.py` if it needs a new one, and rebuild. Checks: `tools/qa/cbp-player-check.js` (the
player check for YouTube players), `tools/qa/hscroll.js`, `python3 tools/og/check_og.py`.

---

## 10. Round 2 (MTG, 22 Nov 2026, live the same day)

MTG: optimise for phones (the Dashboard button overlapped the site title), a menu as rich as Bitcoin Wealth, Bellver and
ALTRUVA (Member Login, a button to get this website, social buttons), 3D and smooth motion without overdoing it, the
compensation plan and the videos easy to reach, copy where every word earns its place, ClickBaitPays positioned as the
traffic source behind everything a visitor already promotes (not an investment), the website copy sold across the site,
headings in the official clickbaitpays.me font (Orbitron), and outranking every other ClickBaitPays site.

| Part | Now |
|---|---|
| Fonts | Orbitron for every heading, cover and preview (as on clickbaitpays.me), Poppins for text |
| Phones | The site title shortens instead of running under the buttons; the quick bar at the bottom: Home, Videos, Join Free, Plan, Menu. New check: `tools/qa/overlap.js` (things lying on each other, at phone widths and with large text) |
| Menu | Pages in 6 groups (Start Here now holds Grow What You Promote and the Compensation Plan), More From MTG (Get This Website, Join The MTG TRIBE), then a grid of 10 buttons: Member Login, Get This Website, Go Home, MTG TRIBE, WhatsApp MTG, Telegram, TikTok, YouTube, Facebook, Disclaimer |
| Money page | /cbp/dashboard/compensation-plan/ (was income-strategy, which forwards): the video, numbers that count up, 3 ways it pays, the 3D staircase of the 7 levels, the table, the 12 + 7 timeline, the presentation and the live Q&A. A gold Plan button in every top bar |
| New pages | Grow What You Promote (the traffic source idea, Ad Campaign or Login Ad, ads that get the click) and Is It Legit? (the facts, what MTG sees, check it yourself in 4 steps; answers bad reviews calmly) |
| Your own copy | Get This Website in the menu, the quick bar end of every page, a band on the main page with a 3D browser showing mtgtribe.com/cbp/yourname, and a rebuilt order page (how it works, pay only if you like it, what you get) |
| Motion | Cards tilt in 3D toward the mouse and catch the light; sections lift into place as they scroll in; the first view rises in; pages glide into each other (view transitions); numbers count up; all of it off with reduced motion |
| Copy | Generic examples of what visitors promote (an affiliate offer, a shop, YouTube, a WhatsApp group), so every personal copy stays right for its owner |

Still waiting: MTG's own explainers and tutorials (placeholders), the Cloudflare account for the videos (see CLAUDE.md).

---

## 11. clickbaitpaysus.com = the same guide (MTG, 22 Nov 2026, live the same day)

MTG: "remove everything that is currently on clickbaitpaysus.com and replace it with the new content ... on mtgtribe.com/cbp
... so that ... the clickbaitpaysus.com website also gets the same updates at the exact same time."

| Part | Now |
|---|---|
| Build | `python3 cbp/_build/build.py` builds /cbp, then `CBP_TARGET=cbpus` builds the guide for the domain root and installs it into `/home/user/clickbaitpays` (MusaTheGiant/clickbaitpays). `--no-cbpus` skips it |
| Addresses | Same paths without /cbp: /dashboard/..., /calculator/, /disclaimer/, /cbpcopy/. Canonical, sitemap, llms.txt, manifest, robots.txt and structured data use clickbaitpaysus.com; MTG's group and other guides keep their mtgtribe.com addresses |
| Previews | Their own set with clickbaitpaysus.com in the pill: `CBP_TARGET=cbpus python3 cbp/_build/og.py` (into `cbp/_build/og-cbpus/`) |
| Order form | On clickbaitpaysus.com the clickbaitpaysus.com/yourname address comes first |
| Old site | Its 28 pages and the /mtg copy (34 addresses) forward to the matching new pages; the old files are in the repo's history |
| Kept | CNAME only; the shared files (video-return.js, mtg-dash.css and .js, wa-message.js, zoom-cta.js) travel with the copy |
